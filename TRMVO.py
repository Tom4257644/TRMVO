import os
import kivy
from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager, NoTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
import matplotlib.pyplot as plt
from kivy.clock import Clock
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.metrics import dp
import mysql.connector
from kivy.uix.widget import Widget
from kivy.config import Config
import pandas as pd
from datetime import date
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty


db_config = {
        'user': 'root',        
        'password': '',          
        'host': 'localhost',     
        'database': 'sonachan' 
    }

kivy.require('2.3.0')

global yearlyData 
yearlyData = {}
user = ''
monthlyPaymentForTransfer = 'empty'
totalInterestForTransfer = ''
housePriceForTransfer = ''
openingEquityForTransfer = ''

# ASSUMPTIONS

managementFees = 'Yes' 
timeValueOfMoney = 'No'
guaranteedTenant = 'No'
costOfCapital = 0.1
locationBeingUpdated = 'Auckland'
aucklandAssumption = {
    'averageRentalGrowthRate': 1.0456,
    'assetPriceIncrease': 1.055,
    'occupancyRisk': 0.97,
    'averageInflationLevel': 1.025,
    'propertyTaxes': 0.0039,
    'managementFee': 0.09,
    'averageMaintenanceCosts': 982
}

christchurchAssumption = {
    'averageRentalGrowthRate': 1.056,
    'assetPriceIncrease': 1.0529,
    'occupancyRisk': 0.98,
    'averageInflationLevel': 1.025,
    'propertyTaxes': 0.0039,
    'managementFee': 0.09,
    'averageMaintenanceCosts': 982

}


# Screens 

class Disclaimer(Screen):
    pass

class LoggedOutScreen(Screen):
    def show_login_message(self):
        login_message_label = self.ids.login_message
        login_message_label.text = "Please log in to continue."

class LogInScreen(Screen):
    def changeLabel(self):
        login_status_label = self.ids.login_status
        login_status_label.text = "Invalid Username or Password"

class AccountScreen(Screen):
    def on_pre_enter(self):
        global db_config
        global user
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(f"SELECT password, email, plan FROM users WHERE username = '{user}'")
        result = cursor.fetchone()
        print(result)
        username_label = self.ids.nameDB
        username_label.text = user
        password_label = self.ids.passwordDB
        password_label.text = result[0]
        email_label = self.ids.emailDB
        email_label.text = result[1]
        plan_label = self.ids.planDB
        plan_label.text = result[2]
        cursor.close()
        conn.close()
    
    def usernameTakenMessage(self, message):
        update_account_message_label = self.ids.update_account_message
        update_account_message_label.text = message

class MenuScreen(Screen):
    pass

class InsightsScreen(Screen):
    def on_pre_enter(self):

        self.ids.stats_layout.clear_widgets()
        self.ids.graphs_layout.clear_widgets()

        # Adding Key Statistics This is the basic stuff but better scraped/API STATS will be inputted.

        stats = [
            "ANZ VF interest rate: 8.64%",
            "ASB VF interest rate: 8.64%",
            "BNZ VF interest rate: 8.69%",
            "The cooperative bank VF interest rate: 8.40%",
            "KiwiBank VF interest rate: 8.50%",
            "SBS VF interest rate: 8.74%",
            "TSB VF interest rate: 8.64%",
            "Westpac VF interest rate: 8.64%",
            "Average Rent for 2 Bedrooms Christchurch:  $455",
            "Average Rent for 3/4 Bedrooms Christchurch:  $550",
            "Average Rent for 1 Bedrooms Auckland:  $490",
            "Average Rent for 2 Bedrooms Auckland:  $650",
            "Average Rent for 3 Bedrooms Auckland:  $800",
            "Average Rent for 4 Bedrooms Auckland:  $995",
            "OCR: 5.50",
            "Tom's Expected 6-Month OCR: 5.50",
        ]

        ocrLevels = [4.5, 4.75, 4.75, 4.75, 4.75]
        monthsOCR = ["Jun 2023", "Sep 2023", "Dec 2023", "Mar 2024", "Jun 2024"]

        # For graph two, first is Y axis the second is X axis 
        ocrLevelsB = [3.5, 2.75, 3.75, 4.75, 6.75] 
        monthsOCR = ["Jun 2023", "Sep 2023", "Dec 2023", "Mar 2024", "Jun 2024"]

        ocrLevelsC = [3.75, 2.75, 6.75, 4.75, 4.75]
        monthsOCR = ["Jun 2023", "Sep 2023", "Dec 2023", "Mar 2024", "Jun 2024"]


        # CREATING THE GRAPHS
        fig, ax = plt.subplots()
        ax.plot(monthsOCR, ocrLevels)  
        graph_path_a = f"graph_a.png"
        plt.savefig(graph_path_a)
        plt.close()
        fig, ax = plt.subplots()
        ax.plot(monthsOCR, ocrLevelsB)  
        graph_path_b = f"graph_b.png"
        plt.savefig(graph_path_b)
        plt.close()
        fig, ax = plt.subplots()
        ax.plot(monthsOCR, ocrLevelsC)  
        graph_path_c = "graph_c.png"
        plt.savefig(graph_path_c)
        plt.close()


        # ADDING THE GRAPHS AND STATS TO KVIY DISPLAY

        for stat in stats:
            self.ids.stats_layout.add_widget(Label(text=stat, font_size=50, color=(0,0,0,1)))
    
        self.ids.graphs_layout.add_widget(Image(source=graph_path_a))
        self.ids.graphs_layout.add_widget(Image(source=graph_path_b))
        self.ids.graphs_layout.add_widget(Image(source=graph_path_c))

class MortgageCalculator(Screen):
    def displayDetails(self, monthlyPayments):
        print('working')
        results_text_label = self.ids.results_text
        results_text_label.text = monthlyPayments

class NewRentalModelScreen(Screen):
        def set_default_values(self):

            if user == 'tom':
                self.ids.property_price.text = "500000"
                self.ids.downpayment.text = "100000"
                self.ids.expected_rent.text = "2000"
                self.ids.mortgage_cost.text = "18000"
                self.ids.total_interest.text = "200000"
            

            global monthlyPaymentForTransfer
            global totalInterestForTransfer
            global housePriceForTransfer
            global openingEquityForTransfer 
            if monthlyPaymentForTransfer != 'empty':
                
                self.ids.property_price.text = str(housePriceForTransfer)
                self.ids.downpayment.text = str(openingEquityForTransfer)
                self.ids.expected_rent.text = ""
                self.ids.mortgage_cost.text = str((monthlyPaymentForTransfer*12))
                self.ids.total_interest.text = str(totalInterestForTransfer)

        def populate_happy_layout(self, displayMessage, *args):

            resultsLabel_label = self.ids.resultsLabel
            resultsLabel_label.text = "Results"
            summaryResults_label = self.ids.summaryResults
            summaryResults_label.text = displayMessage
            self.ids.mainResultsBox.clear_widgets()


            buttons_box = BoxLayout(
                orientation='horizontal',
                spacing=5,
                size_hint=(1, 0.2)
            )


            button1 = Button(
                text="View full summary",
                background_normal='',
                background_color=(0, 0.5, 0, 1),
                font_size=24,  
                size_hint=(1, 0.7),
                valign='middle',
                border_radius=[15],
                
                
            )
            button1.bind(on_press=self.on_button1_press)
            button2 = Button(
                text="Render Full Model",
                background_normal='',
                background_color=(0, 0.5, 0, 1),
                font_size=24,  
                size_hint=(1, 0.7),
                valign='middle',
                border_radius=[15]
            )
            button2.bind(on_press=self.on_button2_press)
            button3 = Button(
                text="Download to EXCEL",
                background_normal='',
                background_color=(0, 0.5, 0, 1),
                font_size=24,  
                size_hint=(1, 0.7),
                valign='middle',
                border_radius=[15]
            )
            button3.bind(on_press=self.on_button3_press)
            buttons_box.add_widget(button1)
            buttons_box.add_widget(button2)
            buttons_box.add_widget(button3)
            results_box_vertical = BoxLayout(
                orientation='vertical',
                spacing=50,
                size_hint=(0.5, 1)
            )
            results_box_vertical.add_widget(buttons_box)
            self.ids.mainResultsBox.add_widget(results_box_vertical)

        def on_button1_press(self, instance):
            app = App.get_running_app()
            app.switchToDisplaySummaryScreen()
        
        def on_button2_press(self, instance):
            app = App.get_running_app()
            app.switchToDisplayFullModelScreen()

        def on_button3_press(self, instance):
            global yearlyData
            app = App.get_running_app()
            app.exportDictToXL(yearlyData)
        
        def displayDownloadMessage(self):
            download_message_label = self.ids.download_message
            download_message_label.text = "Successfully downloaded excel document" 

class DisplayFullModelScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def on_enter(self):
        global yearlyData


        grid = GridLayout(cols=11, padding=[400, 10, 10, 10], spacing=4, size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))
        

        headers = ["", "Y1", "Y2", "Y3", "Y4", "Y5", "Y6", "Y7", "Y8", "Y9", "Y10"]
        for header in headers:
            grid.add_widget(Label(text=header, bold=True, size_hint_y=None, height=dp(30), font_size=dp(14), color=(0, 0, 0, 1)))


        for metric, values in yearlyData.items():
            metric_box = BoxLayout(padding=[0, 0, 0, 0], size_hint_y=None, height=dp(30))
            metric_label = Label(text=metric, size_hint_y=None, padding=[0, 0, 300, 0] ,height=dp(30), font_size=dp(12), color=(0, 0, 0, 1))
            metric_box.add_widget(metric_label)
            grid.add_widget(metric_box)

            for year in range(1, 11):
                value = values[f'y{year}']
                grid.add_widget(Label(text=str(value), size_hint_y=None, height=dp(30), font_size=dp(12), color=(0, 0, 0, 1)))
        
        scrollview = ScrollView(size_hint=(1, None), size=(Window.width-200, Window.height-100))
        scrollview.add_widget(grid)
        self.add_widget(scrollview)

class DisplaySummaryScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def on_enter(self):
        global yearlyData

        grid = GridLayout(cols=11, padding=[400, 10, 10, 10], spacing=4, size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))
        

        headers = ["", "Y1", "Y2", "Y3", "Y4", "Y5", "Y6", "Y7", "Y8", "Y9", "Y10"]
        for header in headers:
            grid.add_widget(Label(text=header, bold=True, size_hint_y=None, height=dp(30), font_size=dp(14), color=(0, 0, 0, 1)))


        for metric, values in yearlyData.items():
            if metric in ['Implied Revenue:', 'Forecast Management Fees:', 'Opening Equity:', 'Closing Equity:', 'Appreciation', 'Closing Equity(%):']:
                continue

            else:
                metric_box = BoxLayout(padding=[0, 0, 0, 0], size_hint_y=None, height=dp(30))
                metric_label = Label(text=metric, size_hint_y=None, padding=[0, 0, 300, 0] ,height=dp(30), font_size=dp(12), color=(0, 0, 0, 1))
                metric_box.add_widget(metric_label)
                grid.add_widget(metric_box)

                for year in range(1, 11):
                    value = values[f'y{year}']
                    grid.add_widget(Label(text=str(value), size_hint_y=None, height=dp(30), font_size=dp(12), color=(0, 0, 0, 1)))

        scrollview = ScrollView(size_hint=(1, None), size=(Window.width-200, Window.height-100))
        scrollview.add_widget(grid)
        self.add_widget(scrollview)
      
class HowToScreen(Screen):
     pass    

class AssumptionsScreen(Screen):
    def on_pre_enter(self):
        global managementFees 
        propertyManagerText_label = self.ids.propertyManagerText
        propertyManagerText_label.text = managementFees
        
        global timeValueOfMoney
        TVMText_label = self.ids.TVMText
        TVMText_label.text = timeValueOfMoney
        
        global guaranteedTenant
        guarenteedTenantText_label = self.ids.guarenteedTenantText
        guarenteedTenantText_label.text = guaranteedTenant
        self.clear_widgets()
        if timeValueOfMoney == 'Yes':
            self.add_widgets()
            bceText_label = self.ids.bce
            bceText_label.text = 'Cost of capital'
            global costOfCapital 
            abcText_label = self.ids.abc
            abcText_label.text = str(costOfCapital)
        elif timeValueOfMoney == 'No':
            self.clear_widgets()
            cost_of_captial_message_label = self.ids.cost_of_captial_message
            cost_of_captial_message_label.text = ''

    def add_widgets(self):
        buttons_box = BoxLayout(
            orientation='horizontal',
            spacing=5,
            size_hint=(0.5, 1)
        )
        
        
        self.inputone = TextInput(
            multiline=False,
            size_hint=(0.5, 0.8),
        )
        
        button = Button(
            text="Set Cost of Capital (%)",
            background_normal='',
            background_color=(0, 0.5, 0, 1),
            font_size=(self.height * 0.03),  
            size_hint=(1, 0.8),
        )

        button.bind(on_press=lambda instance: self.updatecoc(self.inputone.text))
        buttons_box.add_widget(self.inputone)
        buttons_box.add_widget(button)
        results_box_vertical = BoxLayout(
            orientation='vertical',
            spacing=50,
            size_hint=(1, 1)
        )
        results_box_vertical.add_widget(buttons_box)
        self.ids.box.add_widget(results_box_vertical)

    def clear_widgets(self):
        self.ids.box.clear_widgets() 

    def updatecoc(self, house_price_text):
        global costOfCapital 
        house_price_text = str(int(house_price_text)/100)
        costOfCapital = float(house_price_text)
        self.ids.box.clear_widgets()
        

        app = App.get_running_app()
        app.updateCostOfCapitalOnAssumptionsScreen()


        self.changeLabel()

        print(f"Cost of capital updated to: {costOfCapital}")

    def changeLabel(self):
        cost_of_captial_message_label = self.ids.cost_of_captial_message
        cost_of_captial_message_label.text = f"Cost of capital has been set to {costOfCapital}"

class LocationsAssumptionsScreen(Screen):
    def on_pre_enter(self):
        global locationBeingUpdated
        global aucklandAssumption
        global christchurchAssumption
        if locationBeingUpdated == 'Auckland':
            x = aucklandAssumption
        if locationBeingUpdated == 'Christchurch':
            x = christchurchAssumption
        
        cityName_label = self.ids.cityName
        cityName_label.text = f'Update Assumptions for {locationBeingUpdated}'
        averageRentalGrowthRateText_label = self.ids.averageRentalGrowthRateText
        averageRentalGrowthRateText_label.text = str(x['averageRentalGrowthRate'])
        assetPriceIncrease_label = self.ids.assetPriceIncreaseText
        assetPriceIncrease_label.text = str(x['assetPriceIncrease'])
        occupancyRisk_label = self.ids.occupancyRiskText
        occupancyRisk_label.text = str(x['occupancyRisk'])
        averageInflationLevel_label = self.ids.averageInflationLevelText
        averageInflationLevel_label.text = str(x['averageInflationLevel'])
        propertyTaxes_label = self.ids.propertyTaxesText
        propertyTaxes_label.text = str(x['propertyTaxes'])
        managementFee_label = self.ids.managementFeeText
        managementFee_label.text = str(x['managementFee'])
        averageMaintenanceCosts_label = self.ids.averageMaintenanceCostsText
        averageMaintenanceCosts_label.text = str(x['averageMaintenanceCosts'])
            

# Defining the App Object
class TRMVOApp(App):
    Window.size = (1200, 600)

    def build(self):
        sm = ScreenManager(transition=NoTransition())
        sm.add_widget(Disclaimer(name='Disclaimer'))
        sm.add_widget(LoggedOutScreen(name='LoggedOutScreen'))
        sm.add_widget(LogInScreen(name='LogInScreen'))
        sm.add_widget(AccountScreen(name='AccountScreen'))
        sm.add_widget(MenuScreen(name='MenuScreen'))
        sm.add_widget(InsightsScreen(name='insightsscreen')) 
        sm.add_widget(MortgageCalculator(name='MortgageCalculator')) 
        sm.add_widget(NewRentalModelScreen(name='rentalmodelscreen'))
        sm.add_widget(DisplayFullModelScreen(name='DisplayFullModelScreen'))
        sm.add_widget(DisplaySummaryScreen(name='DisplaySummaryScreen'))
        sm.add_widget(HowToScreen(name='HowToScreen'))
        sm.add_widget(AssumptionsScreen(name='AssumptionsScreen'))
        sm.add_widget(LocationsAssumptionsScreen(name='LocationsAssumptionsScreen'))
        
        self.sm = sm
        return sm
    # For Switching Screens

    def switchToLogInScreen(self):
        print('Log In Screen')
        self.sm.current = 'LogInScreen'

    def switchToRentalModelScreen(self):
        print('Rental Model Screen')
        self.sm.current = 'rentalmodelscreen'
    
    def switchToPastModelsScreen(self):
        print('Past Models Screen')

    def switchToAssumptionsScreen(self):
        print('Assumptions Screen')

    def switchToInsightsScreen(self):
        print('Insights Screen')
        self.sm.current = 'insightsscreen'

    def switchToMortgageCalculator(self):
        print('Mortgage Calculator Screen')
        self.sm.current = 'MortgageCalculator'

    def switchToAccountScreen(self):
        print('Account Screen')
        self.sm.current = 'AccountScreen'
    
    def switchToMenuScreen(self):
        print('Menu Screen')
        self.sm.current = 'MenuScreen'

    def switchToLoggedOutScreen(self):
        print('Logged Out Screen')
        self.sm.current = 'LoggedOutScreen'

    def switchToDisplayFullModelScreen(self):
         self.sm.current = 'DisplayFullModelScreen'

    def switchToDisplaySummaryScreen(self):
         self.sm.current = 'DisplaySummaryScreen'

    def switchToHowTo(self):
        self.sm.current = 'HowToScreen'

    def switchToAssumptionsScreen(self):
        self.sm.current = 'AssumptionsScreen'

    def switchToUpdateLocationAssumptions(self, a):
        global locationBeingUpdated
        locationBeingUpdated = a
        self.sm.current = 'LocationsAssumptionsScreen'

    # MAIN MODEL FUNCTION 
    def generateReport(self, propertyPrice, downpayment, expectedRent, mortgageCost, totalInterest, location):
        proportionOfEquityKept = (propertyPrice-downpayment)/(propertyPrice-downpayment+totalInterest)
        if location =='Auckland':
             global aucklandAssumption
             locationAssumptions = aucklandAssumption 

                
        if location =='Christchurch':
             global christchurchAssumption
             locationAssumptions = christchurchAssumption 

        global yearlyData
        
        yearlyData = {
                # Before occupancy risk 
                'impliedRevenue':{
                'y1':0,
                'y2':3,
                'y3':0,
                'y4':0,
                'y5':0,
                'y6':4,
                'y7':0,
                'y8':0,
                'y9':0,
                'y10':0,
                },

                # after accounting for occupancy risk 
                'expectedRevenue':{
                'y1':0,
                'y2':0,
                'y3':0,
                'y4':0,
                'y5':0,
                'y6':0,
                'y7':0,
                'y8':0,
                'y9':0,
                'y10':0,
                },


                'forecastPropertyTaxes':{
                'y1':0,
                'y2':0,
                'y3':0,
                'y4':0,
                'y5':0,
                'y6':0,
                'y7':0,
                'y8':0,
                'y9':0,
                'y10':0,
                },

                'forecastManagementFee':{
                'y1':0,
                'y2':0,
                'y3':0,
                'y4':0,
                'y5':0,
                'y6':0,
                'y7':0,
                'y8':0,
                'y9':0,
                'y10':0,
                },


                # could switch between paying interest and paying equity as well 
                'mortgagePayments':{
                'y1':0,
                'y2':0,
                'y3':0,
                'y4':0,
                'y5':0,
                'y6':0,
                'y7':0,
                'y8':0,
                'y9':0,
                'y10':0,
                },


                'costOfHomeImprovement':{
                'y1':0,
                'y2':0,
                'y3':0,
                'y4':0,
                'y5':0,
                'y6':0,
                'y7':0,
                'y8':0,
                'y9':0,
                'y10':0,
                },


                'totalRentalIncomes':{
                'y1':0,
                'y2':0,
                'y3':0,
                'y4':0,
                'y5':0,
                'y6':0,
                'y7':0,
                'y8':0,
                'y9':0,
                'y10':0,
                },


                'openingCarryingValueOfProperty':{
                'y1':0,
                'y2':0,
                'y3':0,
                'y4':0,
                'y5':0,
                'y6':0,
                'y7':0,
                'y8':0,
                'y9':0,
                'y10':0,
                },

                'Appreciation':{
                'y1':0,
                'y2':0,
                'y3':0,
                'y4':0,
                'y5':0,
                'y6':0,
                'y7':0,
                'y8':0,
                'y9':0,
                'y10':0,
                },

                'openingEquity':{
                'y1':0,
                'y2':0,
                'y3':0,
                'y4':0,
                'y5':0,
                'y6':0,
                'y7':0,
                'y8':0,
                'y9':0,
                'y10':0,
                },


                # from proportion of mortgage paid that is for equity 
                'increaseInEquity':{
                'y1':0,
                'y2':0,
                'y3':0,
                'y4':0,
                'y5':0,
                'y6':0,
                'y7':0,
                'y8':0,
                'y9':0,
                'y10':0,
                },


                'closingEquity':{
                'y1':0,
                'y2':0,
                'y3':0,
                'y4':0,
                'y5':0,
                'y6':0,
                'y7':0,
                'y8':0,
                'y9':0,
                'y10':0,
                },


                'closingProportionOfEquity':{
                'y1':0,
                'y2':0,
                'y3':0,
                'y4':0,
                'y5':0,
                'y6':0,
                'y7':0,
                'y8':0,
                'y9':0,
                'y10':0,
                },


                'totalReturn':{
                'y1':0,
                'y2':0,
                'y3':0,
                'y4':0,
                'y5':0,
                'y6':0,
                'y7':0,
                'y8':0,
                'y9':0,
                'y10':0,
                },


                'totalReturnOnAssetsPercentage':{
                'y1':0,
                'y2':0,
                'y3':0,
                'y4':0,
                'y5':0,
                'y6':0,
                'y7':0,
                'y8':0,
                'y9':0,
                'y10':0,
                }


                }
        for i in yearlyData['impliedRevenue']:
                if i == 'y1':  
                        # incomes pricing
                        yearlyData['impliedRevenue']['y1'] = expectedRent*52

                        yearlyData['costOfHomeImprovement']['y1'] = (locationAssumptions['averageMaintenanceCosts'])
                        # asset appreciation pricing
                        yearlyData['openingCarryingValueOfProperty']['y1'] = propertyPrice
                        yearlyData['openingEquity']['y1'] = downpayment
                        h = i
                else:
                        yearlyData['impliedRevenue'][i] = yearlyData['impliedRevenue'][h] * locationAssumptions['averageRentalGrowthRate']
                        yearlyData['costOfHomeImprovement'][i] = yearlyData['costOfHomeImprovement'][h]*locationAssumptions['averageInflationLevel']
                        # asset appreciation pricing 
                        yearlyData['openingCarryingValueOfProperty'][i] = yearlyData['openingCarryingValueOfProperty'][h]*locationAssumptions['assetPriceIncrease']
                        yearlyData['Appreciation'][h] = yearlyData['openingCarryingValueOfProperty'][i] - yearlyData['openingCarryingValueOfProperty'][h]
                        yearlyData['openingEquity'][i] = yearlyData['closingEquity'][h]
                        h = i
                if guaranteedTenant == 'Yes':
                    yearlyData['expectedRevenue'][i] = yearlyData['impliedRevenue'][i]
                else:
                    yearlyData['expectedRevenue'][i] = yearlyData['impliedRevenue'][i]*locationAssumptions['occupancyRisk']
                yearlyData['forecastPropertyTaxes'][i] = yearlyData['openingCarryingValueOfProperty'][i]*locationAssumptions['propertyTaxes']
                if managementFees == 'Yes':
                    yearlyData['forecastManagementFee'][i] = yearlyData['expectedRevenue'][i]*locationAssumptions['managementFee']
                yearlyData['mortgagePayments'][i] = mortgageCost
                # asset appreciation pricing
                yearlyData['increaseInEquity'][i] = yearlyData['expectedRevenue'][i]*proportionOfEquityKept
                yearlyData['closingEquity'][i] = yearlyData['increaseInEquity'][i]+yearlyData['openingEquity'][i]
                yearlyData['closingProportionOfEquity'][i] = (yearlyData['closingEquity'][i])/(yearlyData['openingCarryingValueOfProperty'][i])

        for i in yearlyData['totalRentalIncomes']:
                yearlyData['totalRentalIncomes'][i] = (yearlyData['expectedRevenue'][i]) - (yearlyData['forecastPropertyTaxes'][i]) - (yearlyData['forecastManagementFee'][i]) - (yearlyData['mortgagePayments'][i]) - (yearlyData['costOfHomeImprovement'][i])
                yearlyData['totalReturn'][i] = yearlyData['increaseInEquity'][i]+(yearlyData['totalRentalIncomes'][i])
                yearlyData['totalReturnOnAssetsPercentage'][i] = yearlyData['totalReturn'][i]/(yearlyData['openingEquity'][i])

        if managementFees == 'No':
            del yearlyData['forecastManagementFee']

        cocmessage = ''
        if timeValueOfMoney == 'Yes':
            yearlyData['discountedToTodayMoney'] = {}
            global costOfCapital


            x = 1
            presentValueOfTotalCashFlows = 0
            for year in yearlyData['impliedRevenue']:
                yearlyData['discountedToTodayMoney'][year] = yearlyData['totalReturn'][year] / ((1+costOfCapital)**x)
                presentValueOfTotalCashFlows = presentValueOfTotalCashFlows + yearlyData['discountedToTodayMoney'][year]
                x = x+1
    
            if presentValueOfTotalCashFlows>0:
                presentValueOfTotalCashFlows = round(presentValueOfTotalCashFlows, 2)

                cocmessage = f'Taking into account your cost of capital of {(costOfCapital*100)}%, this property would exceed it (by ${presentValueOfTotalCashFlows} at today\'s dollar value over the first ten years), which means you should buy the property and begin renting it out as soon as possible, We recommend downloading the summary to excel and taking to a bank to begin the mortgage application'
            if presentValueOfTotalCashFlows<0:

                cocmessage = f'Taking into account your cost of capital of {(costOfCapital*100)}%, this property would not meet your required returns, we recommend you do not purchase this property and you continue searching for more properties.'



        for key, nested_dict in yearlyData.items():
                for nested_key, value in nested_dict.items():
                        if isinstance(value, (int, float)):
                                yearlyData[key][nested_key] = round(value, 2)

        sumTotalsReturn = 0 
        for i in yearlyData['totalReturnOnAssetsPercentage']:
             sumTotalsReturn = sumTotalsReturn + yearlyData['totalReturnOnAssetsPercentage'][i]
             
        averageReturn = sumTotalsReturn/10
        averageReturn = round(averageReturn, 2)
        a = yearlyData['totalRentalIncomes']['y1']
        
        if (a) > 0:
            cashFlowMessage = f"You can expect this property to be cash flow positive year one, of ${yearlyData['totalRentalIncomes']['y1']}, so you will not have to contribute any extra to cover the mortgage payments, you should be able to rely on rental incomes."
        else: 
            cashFlowMessage = f"You can expect this property to be cash flow negative year one \nThis means you will have to contribute ${yearlyData['totalRentalIncomes']['y1']} year one, this is likely to be reoccuring every year"

            

        displayMessage = f"The average return over the next ten years will be {(averageReturn*100)}%\nThe first year's return will be ${yearlyData['totalReturn']['y1']} which is a ROA of {(yearlyData['totalReturnOnAssetsPercentage']['y1']*100)}%\n{cashFlowMessage}\n{cocmessage}"

        print(displayMessage)
        NewRentalModelScreen = self.sm.get_screen('rentalmodelscreen')
        NewRentalModelScreen.populate_happy_layout(displayMessage)

        new_key = 'Implied Revenue:'
        yearlyData[new_key] = yearlyData.pop('impliedRevenue')


        new_key = 'Expected Revenue:'
        yearlyData[new_key] = yearlyData.pop('expectedRevenue')

        new_key = 'Forecast Property Taxes:'
        yearlyData[new_key] = yearlyData.pop('forecastPropertyTaxes')

        if managementFees == 'Yes':
            new_key = 'Forecast Management Fees:'
            yearlyData[new_key] = yearlyData.pop('forecastManagementFee')

        new_key = 'Mortgage Payments:'
        yearlyData[new_key] = yearlyData.pop('mortgagePayments')


        new_key = 'Cost of Home Improvement:'
        yearlyData[new_key] = yearlyData.pop('costOfHomeImprovement')

        new_key = 'Total Rental Incomes:'
        yearlyData[new_key] = yearlyData.pop('totalRentalIncomes')


        new_key = 'Property Opening Value:'
        yearlyData[new_key] = yearlyData.pop('openingCarryingValueOfProperty')

        new_key = 'Appreciation:'
        yearlyData[new_key] = yearlyData.pop('Appreciation')


        new_key = 'Opening Equity:'
        yearlyData[new_key] = yearlyData.pop('openingEquity')

        new_key = 'Increase in Equity:'
        yearlyData[new_key] = yearlyData.pop('increaseInEquity')


        new_key = 'Closing Equity:'
        yearlyData[new_key] = yearlyData.pop('closingEquity')

        new_key = 'Closing Equity(%):'
        yearlyData[new_key] = yearlyData.pop('closingProportionOfEquity')

        new_key = 'Total Return:'
        yearlyData[new_key] = yearlyData.pop('totalReturn')

        new_key = 'Total ROA (%):'
        yearlyData[new_key] = yearlyData.pop('totalReturnOnAssetsPercentage')
     
    def mortgageCalculator(self, housePrice, deposit, loanTermYears, loanTermMonths, interestRate):
        loanInYears = ((loanTermYears*12)+loanTermMonths)/12
        totalPaymentsMonthly = loanInYears*12
        interestRateDecimal = interestRate/100
        prinipal = housePrice - deposit
        x = (1 +(interestRateDecimal/12))**(-12*30)
        monthlyPayment = (prinipal*(interestRateDecimal/12))/(1-x)
        totalPaid = monthlyPayment*totalPaymentsMonthly
        totalInterest = totalPaid-prinipal
        monthlyPayment = round(monthlyPayment, 2)
        totalPaymentsMonthly = round(totalPaymentsMonthly, 2)
        prinipal = round(prinipal, 2)
        totalInterest = round(totalInterest, 2)
        totalPaid = round(totalPaid, 2)
        global monthlyPaymentForTransfer
        global totalInterestForTransfer
        global housePriceForTransfer
        global openingEquityForTransfer 
        monthlyPaymentForTransfer = monthlyPayment
        totalInterestForTransfer = totalInterest
        housePriceForTransfer = housePrice
        openingEquityForTransfer = deposit
        message = (f"The Monthly Payment will be {monthlyPayment}\nThe total number of payments will be {totalPaymentsMonthly}\nThe total loan amount is {prinipal}\nThe total interest will be {totalInterest}\nThe total amount paid will be {totalPaid}")
        MortgageCalculator = self.sm.get_screen('MortgageCalculator')
        MortgageCalculator.displayDetails(message)

    def processLogIn(self, username, password):
        valid = False
        global db_config
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()


        
        cursor.execute(f"SELECT username FROM users WHERE username = '{username}'")
        result = cursor.fetchone()
        if result:
            cursor.execute(f"SELECT password FROM users WHERE username = '{username}'")
            result = cursor.fetchone()
            if result[0] == password:
                 valid = True
        else:
            valid = False


        cursor.close()
        conn.close()

        if valid: 
            self.sm.current = 'MenuScreen'
            global user
            user = username
        else:
            login_screen = self.sm.get_screen('LogInScreen')
            login_screen.changeLabel()

    def exportDictToXL(self, dict):
        df = pd.DataFrame(data=dict)
        df = (df.T)
        print (df)
        today = date.today()
        df.to_excel(f'{user}-TRMVOModel-{today}.xlsx')

        model_screen = self.sm.get_screen('rentalmodelscreen')
        model_screen.displayDownloadMessage()

    # UPDATING ACCOUNT DETAILS
    def updateUsername(self, newUsername):
        global db_config
        global user
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(f"SELECT username FROM users WHERE username = '{newUsername}'")
        result = cursor.fetchone()
        if result:
            print('username taken')
            AccountScreen = self.sm.get_screen('AccountScreen')
            AccountScreen.usernameTakenMessage("Username is already taken")
            
        else:
            query = "UPDATE users SET username = %s WHERE username = %s"
            cursor.execute(query, (newUsername, user))
            conn.commit()
            user = newUsername
            AccountScreen = self.sm.get_screen('AccountScreen')
            AccountScreen.usernameTakenMessage('')

        cursor.close()
        conn.close()
        self.sm.current = 'LoggedOutScreen'
        self.sm.current = 'AccountScreen'
         
    def updatePassword(self, newPassword):
        global db_config
        global user
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        query = "UPDATE users SET password = %s WHERE username = %s"
        cursor.execute(query, (newPassword, user))
        conn.commit()
        cursor.close()
        conn.close()
        self.sm.current = 'LoggedOutScreen'
        self.sm.current = 'AccountScreen'

    def updateEmail(self, newEmail):
        global db_config
        global user
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(f"SELECT email FROM users WHERE email = '{newEmail}'")
        result = cursor.fetchone()
        if result:
             print('email taken')
        else:
            query = "UPDATE users SET email = %s WHERE username = %s"
            cursor.execute(query, (newEmail, user))
            conn.commit()

        cursor.close()
        conn.close()
        self.sm.current = 'LoggedOutScreen'
        self.sm.current = 'AccountScreen'
        
    # UPDATING THE ASSUMPTIONS

    def updateManagementFeeAssumption(self, yn):
        print(yn)
        global managementFees
        managementFees = yn
        self.sm.current = 'LoggedOutScreen'
        self.sm.current = 'AssumptionsScreen'

    def updatetimeValueOfMoneyAssumption(self, yn):
        print(yn)
        global timeValueOfMoney
        timeValueOfMoney = yn
        self.sm.current = 'LoggedOutScreen'
        self.sm.current = 'AssumptionsScreen'

    def updateguaranteedTenantAssumption(self, yn):
        print(yn)
        global guaranteedTenant
        guaranteedTenant = yn
        self.sm.current = 'LoggedOutScreen'
        self.sm.current = 'AssumptionsScreen'

    def updateCostOfCapitalOnAssumptionsScreen(self):
        self.sm.current = 'LoggedOutScreen'
        self.sm.current = 'AssumptionsScreen'

    def updateLocationSpecifics(self, x,y):
        x = int(x)
        y = y
        global aucklandAssumption
        global christchurchAssumption
        global locationBeingUpdated
        if locationBeingUpdated == 'Auckland':
            aucklandAssumption[y] = x
        if locationBeingUpdated == 'Christchurch':
            christchurchAssumption[y] = x
        self.sm.current = 'AssumptionsScreen'
        self.sm.current = 'LocationsAssumptionsScreen'
        



if __name__ == '__main__':
    TRMVOApp().run()