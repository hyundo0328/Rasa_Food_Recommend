from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import mysql.connector


global ingredient_info
foodName_str = ""


# 입력한 식재료, 칼로리 slot 추출
class ActionSaveSlotIngredient(Action):
    def name(self) -> Text:
        return "action_save_slot_ingredient"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # 슬롯 추출
        ingredient = next(tracker.get_latest_entity_values("ingredient_info"), None)
        # 전역 변수로 저장
        global ingredient_info
        ingredient_info = ingredient

        dispatcher.utter_message(text=f"The ingredient you have is {ingredient}.\n")
        dispatcher.utter_message(text="\nThe ingredient information you entered has been saved.\n"
                                      "\nWrite down the calories you want. (Ex: High, Low)")

        # SlotSet(key="ingredient", value=ingredient)
        return []


# 첫 번째 추천 음식 DB에서 찾기
class ActionFirstRecommendFood(Action):
    def name(self) -> Text:
        return "action_first_recommend_food"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # 슬롯 추출
        kcalSave = next(tracker.get_latest_entity_values("kcal_info"), None)

        dispatcher.utter_message(text=f"You want {kcalSave} calories.\n")

        # MySQL 데이터베이스 연결 설정
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="root1234",
            database="food",
            port='3306'
        )

        cursor = conn.cursor()

        query = f"SELECT foodName, foodIngredient, kcal FROM foodrecipe WHERE foodIngredient like '%{ingredient_info}%' and kcal like '{kcalSave}' order by rand() limit 3"

        # 쿼리 실행
        cursor.execute(query)

        # 조회한 음식 목록을 담을 리스트 생성
        food_list = []

        global foodName_str
        foodName_str = ""
        for row in cursor.fetchall():
            foodName = row[0]
            foodName_str += foodName+", "
            foodIngredient = row[1]
            kcal = row[2]

            food_info = "Food Name: {0}, Ingredient: {1}, Kcal: {2}".format(foodName, foodIngredient, kcal)
            food_list.append(food_info)

        # 커넥션 및 커서 닫기
        cursor.close()
        conn.close()

        # 첫 번째 추천 음식 출력
        if food_list:
            food_text = " \nBased on your input, I will recommend you up to 3 foods.\n"
            food_text += "\n".join(food_list)
            food_text += "\n \nIf you are satisfied with any food, please write down the exact name of the food or order."
            food_text += "\n(Ex: Food Name, First, Second, Third)"
            food_text += "\nIf you don't have any food you want, please enter a negative word. (Ex: No, Tell me another food)"
            dispatcher.utter_message(text=food_text)
        else:
            dispatcher.utter_message(text="There is no food that can be made with the ingredients you have.")

        return []


# 두 번째 추천 음식 DB에서 찾기
class ActionSecondRecommendFood(Action):
    def name(self) -> Text:
        return "action_second_recommend_food"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # 슬롯 추출
        timeSave = next(tracker.get_latest_entity_values("time_info"), None)
        timeSave = int(timeSave)

        dispatcher.utter_message(text=f"You can use {timeSave} minutes for cooking time.\n")

        # MySQL 데이터베이스 연결 설정
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="root1234",
            database="food",
            port='3306'
        )

        cursor = conn.cursor()

        query = f"SELECT foodName, foodIngredient, cookingTime FROM foodrecipe WHERE foodIngredient like '%{ingredient_info}%' and cookingTime <= {timeSave} order by rand() limit 3"

        # 쿼리 실행
        cursor.execute(query)

        # 조회한 음식 목록을 담을 리스트 생성
        food_list = []

        global foodName_str
        foodName_str = ""
        for row in cursor.fetchall():
            foodName = row[0]
            foodName_str += foodName + ", "
            foodIngredient = row[1]
            cookingTime = row[2]

            food_info = "Food Name: {0}, Ingredient: {1}, Cooking Time: {2} minutes".format(foodName, foodIngredient,
                                                                                            cookingTime)
            food_list.append(food_info)

        # 커넥션 및 커서 닫기
        cursor.close()
        conn.close()

        # 첫 번째 추천 음식 출력
        if food_list:
            food_text = " \nBased on your input, I will recommend you up to 3 foods.\n"
            food_text += "\n".join(food_list)
            food_text += "\n \nIf you are satisfied with any food, please write down the exact name of the food or order."
            food_text += "\n(Ex: Food Name, First, Second, Third)"
            dispatcher.utter_message(text=food_text)
        else:
            dispatcher.utter_message(text="There is no food that can be made with the ingredients you have.")

        return []


# 세 번째 추천 음식 DB에서 찾기
class ActionThirdRecommendFood(Action):
    def name(self) -> Text:
        return "action_third_recommend_food"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # 슬롯 추출
        originSave = next(tracker.get_latest_entity_values("origin_info"), None)

        dispatcher.utter_message(text=f"You want {originSave} food.\n")

        # MySQL 데이터베이스 연결 설정
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="root1234",
            database="food",
            port='3306'
        )

        cursor = conn.cursor()

        query = f"SELECT foodName, foodIngredient, origin FROM foodrecipe WHERE foodIngredient like '%{ingredient_info}%' and origin like '{originSave}' order by rand() limit 3"

        # 쿼리 실행
        cursor.execute(query)

        # 조회한 음식 목록을 담을 리스트 생성
        food_list = []

        global foodName_str
        foodName_str = ""
        for row in cursor.fetchall():
            foodName = row[0]
            foodName_str += foodName + ", "
            foodIngredient = row[1]
            origin = row[2]

            food_info = "Food Name: {0}, Ingredient: {1}, Country: {2}".format(foodName, foodIngredient, origin)
            food_list.append(food_info)

        # 커넥션 및 커서 닫기
        cursor.close()
        conn.close()

        # 첫 번째 추천 음식 출력
        if food_list:
            food_text = " \nBased on your input, I will recommend you up to 3 foods.\n"
            food_text += "\n".join(food_list)
            food_text += "\n \nIf you are satisfied with any food, please write down the exact name of the food or order."
            food_text += "\n(Ex: Food Name, First, Second, Third)"
            dispatcher.utter_message(text=food_text)
        else:
            dispatcher.utter_message(text="There is no food that can be made with the ingredients you have.")

        return []


# 네 번째 추천 음식 DB에서 찾기
class ActionFourthRecommendFood(Action):
    def name(self) -> Text:
        return "action_fourth_recommend_food"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # 슬롯 추출
        allergy = next(tracker.get_latest_entity_values("allergy_info"), None)

        dispatcher.utter_message(text=f"Your ingredient enter {allergy}\n")

        # MySQL 데이터베이스 연결 설정
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="root1234",
            database="food",
            port='3306'
        )

        cursor = conn.cursor()

        if (allergy.lower() == "None".lower()):
            query = f"SELECT foodName, foodIngredient, allergy FROM foodrecipe WHERE foodIngredient like '%{ingredient_info}%' order by rand() limit 3"
        else:
            query = f"SELECT foodName, foodIngredient, allergy FROM foodrecipe WHERE foodIngredient like '%{ingredient_info}%' and allergy not like '%{allergy}%' order by rand() limit 3"

        # 쿼리 실행
        cursor.execute(query)

        # 조회한 음식 목록을 담을 리스트 생성
        food_list = []

        global foodName_str
        foodName_str = ""
        for row in cursor.fetchall():
            foodName = row[0]
            foodName_str += foodName + ", "
            foodIngredient = row[1]
            allergy = row[2]

            food_info = "Food Name: {0}, Ingredient: {1}, Allergy: {2}".format(foodName, foodIngredient, allergy)
            food_list.append(food_info)

        # 커넥션 및 커서 닫기
        cursor.close()
        conn.close()

        # 첫 번째 추천 음식 출력
        if food_list:
            food_text = " \nThese are foods that do not affect the allergy.\n"
            food_text += "\n".join(food_list)
            food_text += "\n \nIf you are satisfied with any food, please write down the exact name of the food or order."
            food_text += "\n(Ex: Food Name, First, Second, Third)"
            dispatcher.utter_message(text=food_text)
        else:
            dispatcher.utter_message(text="There is no food that can be made with the ingredients you have.")

        return []


# 만족하여 음식 레시피 설명
class ActionDescriptionRecipe(Action):
    def name(self) -> Text:
        return "action_desc_recipe"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # 슬롯 추출
        foodSave = next(tracker.get_latest_entity_values("food_info"), None)

        # MySQL 데이터베이스 연결 설정
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="root1234",
            database="food",
            port='3306'
        )

        cursor = conn.cursor()

        global foodName_str
        foodName_list = foodName_str.split(", ")
        if (foodSave.lower() == "First".lower()):
            query = f"SELECT foodName, recipe FROM foodrecipe WHERE foodName like '{foodName_list[0]}'"
        elif (foodSave.lower() == "Second".lower()):
            query = f"SELECT foodName, recipe FROM foodrecipe WHERE foodName like '{foodName_list[1]}'"
        elif (foodSave.lower() == "Third".lower()):
            query = f"SELECT foodName, recipe FROM foodrecipe WHERE foodName like '{foodName_list[2]}'"
        else:
            query = f"SELECT foodName, recipe FROM foodrecipe WHERE foodName like '{foodSave}' order by rand() limit 3"

        # 쿼리 실행
        cursor.execute(query)

        food_info = ""
        for row in cursor.fetchall():
            foodName = row[0]
            recipe = row[1]

            food_info = "Let me tell you the recipe for the {0}.\n " \
                        "\n{1}".format(foodName, recipe)

        # 커넥션 및 커서 닫기
        cursor.close()
        conn.close()

        # 첫 번째 추천 음식 출력
        if food_info:
            dispatcher.utter_message(text=food_info)
        else:
            dispatcher.utter_message(text="There is no food that can be made with the ingredients you have.")

        return []
