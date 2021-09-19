from django.shortcuts import render
from django.http import HttpResponse

from flask import Flask
from flask_bootstrap import Bootstrap
import numpy as np
import pandas as pd
from joblib import load

from sklearn.ensemble import RandomForestRegressor


app = Flask(__name__)
Bootstrap(app)

cars = pd.read_csv('app/static/FinalCarData.csv')
model_joblib = load('app/static/model.joblib')
lookup_table_df = pd.read_csv('app/static/EncodedCarsLookupTable_df.csv')

# Constants

MAKE_COL = 'manufacturer'
MODEL_COL = 'model'
AGE_COL = 'age'

FUEL_COL = 'fuel'
TRANSM_COL = 'transmission'
TYPE_COL = 'type'
COLOR_COL = 'paint_color'

cookie_exiration = 3600


def index(request):
    """
    This method starts the application and renders index.html.

    :param HttpRequest request: None
    :return:  **render** (*HttpResponse*) - request object, template name.
    """

    return render(request, "index.html")


def reset(request):
    """
    This method resets all the information in the cookies, the dropdown controls and the users selections in green,
    next to the dropdown controls. It keeps the current makes already stored in the cookie.


    :param HttpRequest request: None
    :return:  **render** (*HttpResponse*) - request object, template name, and context (dictionary of values) - the scroll command for the users convenience.
    """

    context = {
        'form_scroll': 'True'
    }

    response = render(request, "car-price-predictor.html", context)

    response.delete_cookie('sel_make')
    response.delete_cookie('sel_model')
    response.delete_cookie('sel_age')
    response.delete_cookie('sel_odometer')
    response.delete_cookie('sel_fuel')
    response.delete_cookie('sel_transm')
    response.delete_cookie('sel_type')
    response.delete_cookie('sel_color')

    response.delete_cookie('ages')
    response.delete_cookie('colors')
    response.delete_cookie('fuels')
    response.delete_cookie('odometers')
    response.delete_cookie('models')
    response.delete_cookie('transmissions')
    response.delete_cookie('types')

    return response


def predictor(request):
    """
        This method is called when the user clicks the link to take them to the predictor part of the application.
        It gets the list of unique makes of the cars in the dataframe and creates a string with a separating character to
        stored in a cookie.

        :param HttpRequest request: None
        :return:  **render** (*HttpResponse*) - request object, template name, and context (dictionary of values)

    """

    # Forward the user to the used car price prediction part of the application
    # and sends the list of cars in the dataset#

    makes_list = cars[MAKE_COL].unique()

    response = render(request, "car-price-predictor.html", )

    makes_list = '|'.join(makes_list)

    response.set_cookie('makes', makes_list, max_age=cookie_exiration)

    return response


def manufacturer(request):
    """
    This method is called when the user selects the manufacturer of the car they would like the price of.
    It takes the selection and finds all the models associated with the selected manufacturer. Then turns the list into a
    string with a separating character and stores the information in a cookie.
    Also saving the manufacture selection in a cookie.

    :param HttpRequest request: None
    :return:  **render** (*HttpResponse*) - request object, template name, and context (dictionary of values) - the scroll command for the users convenience.

    """
    if request.method == 'POST':
        # Get the selection #
        make_selected = request.POST.get("make", "")

        # search the cars to find the selected make
        manuf = cars.loc[cars[MAKE_COL] == make_selected]
        # Find all the models that go with the selected make
        unique_manuf_models = manuf['model'].unique()
        unique_manuf_models.tolist()

        # Take the option of selecting "nan" out of the options
        models_list = [i for i in unique_manuf_models if str(i) != 'nan']

        context = {
            'form_scroll': 'True'
        }

        response = render(request, "car-price-predictor.html", context)

        models_list = '|'.join(models_list)

        response.set_cookie('models', models_list, max_age=cookie_exiration)
        response.set_cookie('sel_make', make_selected, max_age=cookie_exiration)

        return response


def model(request):
    """
    This method is called when the user selects the model of the car they would like the price of.
    It takes the selection and finds all the fuel types associated with the selected car model. Then turns the list into a
    string with a separating character and stores the information in a cookie.
    Also saving the model selection in a cookie. Further, it makes a list of the ages of the cars, turns it into a
    string with a separating character and stores them in a cookie.

    :param HttpRequest request: None
    :return:  **render** (*HttpResponse*) - request object, template name, and context (dictionary of values) - the scroll command for the users convenience.

    """
    if request.method == 'POST':
        # storing for the prediction
        model_selected = request.POST.get("model", "")

        # search the cars with the selected makes and models
        cars_w_make_model = cars[(cars[MAKE_COL] == request.COOKIES.get('sel_make')) &
                                 (cars[MODEL_COL] == model_selected)]

        # Start to prepare stuff for the next selection based on previous information
        # of the cars with the same make and model set fuel type.#

        fuel_list = cars_w_make_model[FUEL_COL].unique()
        fuel_list.tolist()

        # take nan and other out of the options.

        fuel_list = no_nan_other(fuel_list)

        ages_list = list(range(0, 13))

        context = {
            'form_scroll': 'True'
        }

        response = render(request, "car-price-predictor.html", context)

        ages_list = [str(i) for i in ages_list]

        ages_list = '|'.join(ages_list)
        response.set_cookie('ages', ages_list, max_age=cookie_exiration)

        fuel_list = '|'.join(fuel_list)
        response.set_cookie('fuels', fuel_list, max_age=cookie_exiration)

        response.set_cookie('sel_model', model_selected, max_age=cookie_exiration)

        return response


def age(request):
    """
    This method is called when the user selects the age of the car they would like the price of.
    It takes the selected age and stores the information in a cookie. It creates a list of odometer readings for the
    user to choose from and stores those selections in a cookie in the format of a character seperated string.

    :param HttpRequest request: None
    :return:  **render** (*HttpResponse*) - request object, template name, and context (dictionary of values) - the scroll command for the users convenience.

    """
    if request.method == 'POST':
        # store the selected age
        age_selected = request.POST.get("age", "")

        # give the user options to pick the mileage
        uniq_odometer_readings = list(range(1000, 90001, 500))

        uniq_odometer_readings = [str(i) for i in uniq_odometer_readings]

        context = {
            'form_scroll': 'True'
        }

        response = render(request, "car-price-predictor.html", context)

        uniq_odometer_readings = '|'.join(uniq_odometer_readings)

        response.set_cookie('odometers', uniq_odometer_readings, max_age=cookie_exiration)

        response.set_cookie('sel_age', age_selected, max_age=cookie_exiration)

        return response


def odometer(request):
    """
    This method is called when the user selects the odometer reading of the car they would like the price of.
    Takes the selected odometer reading and stores the information in a cookie.

    :param HttpRequest request: None
    :return:  **render** (*HttpResponse*) - request object, template name, and context (dictionary of values) - the scroll command for the users convenience.
    """
    if request.method == 'POST':
        # store the selected odometer reading
        odomtr_selected = request.POST.get("odometer", "")

        context = {
            'form_scroll': 'True'
        }

        response = render(request, "car-price-predictor.html", context)

        response.set_cookie('sel_odometer', odomtr_selected, max_age=cookie_exiration)

        return response


def fuel(request):
    """
    This method is called when the user selects the fuel type of the car they would like the price of.
    It takes the selected fuel type and stores the information in a cookie. Then based on the user selection of the
    manufacturer, model and fuel type searches for the type of transmissions that are available for that car and
    stores them in a cookie by a character separating string.

    :param HttpRequest request: None
    :return:  **render** (*HttpResponse*) - request object, template name, and context (dictionary of values) - the scroll command for the users convenience.
    """
    if request.method == 'POST':
        fuel_selected = request.POST.get("fuel", "")

        # search the cars with the selected makes, models and fuel types
        cars_w_make_model_fuel = cars[
            (cars[MODEL_COL] == request.COOKIES.get('sel_model')) &
            (cars[MAKE_COL] == request.COOKIES.get('sel_make')) &
            (cars[FUEL_COL] == fuel_selected)
            ]

        # get the transmission type - there are not that many
        uniq_transm_types = cars_w_make_model_fuel[TRANSM_COL].unique()
        uniq_transm_types.tolist()

        # no option for nan or other
        uniq_transm_types = no_nan_other(uniq_transm_types)

        context = {
            'form_scroll': 'True'
        }

        response = render(request, "car-price-predictor.html", context)

        uniq_transm_types = '|'.join(uniq_transm_types)
        response.set_cookie('transmissions', uniq_transm_types, max_age=cookie_exiration)

        response.set_cookie('sel_fuel', fuel_selected, max_age=cookie_exiration)

        return response


def transmission(request):
    """
    This method is called when the user selects the transmission type of the car they would like the price of.
    It takes the selected transmission type and stores the information in a cookie. Then based on the user selection of the
    manufacturer, model, fuel type, and transmission type selected searches for the type of cars that are available for that car and
    stores them in a cookie by a character separating string.

    :param HttpRequest request: None
    :return:  **render** (*HttpResponse*) - request object, template name, and context (dictionary of values) - the scroll command for the users convenience.
    """
    if request.method == 'POST':
        transm_selected = request.POST.get("transmission", "")

        # search the cars with the selected makes, models, cylinders and condition
        cars_w_make_model_cond = cars[(cars[MODEL_COL] == request.COOKIES.get('sel_model')) &
                                      (cars[MAKE_COL] == request.COOKIES.get('sel_make')) &
                                      (cars[FUEL_COL] == request.COOKIES.get('sel_fuel')) &
                                      (cars[TRANSM_COL] == transm_selected)
                                      ]

        uniq_types = cars_w_make_model_cond[TYPE_COL].unique()
        uniq_types.tolist()

        uniq_types = no_nan_other(uniq_types)

        context = {
            'form_scroll': 'True'
        }

        response = render(request, "car-price-predictor.html", context)

        uniq_types = '|'.join(uniq_types)
        response.set_cookie('types', uniq_types, max_age=cookie_exiration)

        response.set_cookie('sel_transm', transm_selected, max_age=cookie_exiration)

        return response


def types(request):
    """
    This method is called when the user selects the type of the car they would like the price of.
    It takes the selected type and stores the information in a cookie. Then based on the user selection of the
    manufacturer, model, fuel type, transmission type, and type of car selected, searches for the colors available for that car and
    stores them in a cookie by a character separating string.

    :param HttpRequest request: None
    :return:  **render** (*HttpResponse*) - request object, template name, and context (dictonary of values) - the scroll command for the users convenience.
    """
    if request.method == 'POST':
        type_selected = request.POST.get("type", "")

        # search the cars with the selected makes, models, cylinders and condition
        cars_with_selected = cars[(cars[MODEL_COL] == request.COOKIES.get('sel_model')) &
                                  (cars[MAKE_COL] == request.COOKIES.get('sel_make')) &
                                  (cars[FUEL_COL] == request.COOKIES.get('sel_fuel')) &
                                  (cars[TRANSM_COL] == request.COOKIES.get('sel_transm')) &
                                  (cars[TYPE_COL] == type_selected)
                                  ]

        uniq_colors = cars_with_selected[COLOR_COL].unique()
        uniq_colors.tolist()

        uniq_colors = [i for i in uniq_colors if str(i) != 'nan']

        context = {
            'form_scroll': 'True'
        }

        response = render(request, "car-price-predictor.html", context)

        uniq_colors = '|'.join(uniq_colors)
        response.set_cookie('colors', uniq_colors, max_age=cookie_exiration)

        response.set_cookie('sel_type', type_selected, max_age=cookie_exiration)

        return response


def color(request):
    """
    This method is called when the user selects the color of car they would like the price of.
    It takes the selected color and stores the information in a cookie.

    :param HttpRequest request: None
    :return:  **render** (*HttpResponse*) - request object, template name, and context (dictonary of values) - a different scroll command for the user to see the prediction and enable the prediction button.
    """
    if request.method == 'POST':
        color_selected = request.POST.get("color", "")

        context = {
            'form_scroll': 'True',
            'submit_disabled': 'False',
            'enable_pred_button': True
        }

        response = render(request, "car-price-predictor.html", context)

        response.set_cookie('sel_color', color_selected, max_age=cookie_exiration)

        return response


def getAttr(selected, col_str):
    """
    This method was formed to save room. This method turns the name in to the designated number or index when the
    model was trained.

    :param String selected: Selected attribute
    :param String col_str: The name of the column
    :return:  **index** (*Integer*) - The index number that the string was assigned when the model was trained.
    """
    return lookup_table_df.index[lookup_table_df[col_str] == selected].item()


def prediction(request):
    """
    This method is called when the user presses the prediction button. It takes all the selections they made and converts
    the strings into the assigned numbers when the model was trained. All the assigned number go into a one line
    dataframe and fed into the prediction model for a price prediction of the used car.

    :param HttpRequest request: None
    :return:  **render** (*HttpResponse*) - request object, template name, and context (dictonary of values) - a different scroll command for the user to see the prediction results.
    """
    if request.method == 'POST':
        make_sel = request.COOKIES.get('sel_make')
        model_sel = request.COOKIES.get('sel_model')
        age_sel = request.COOKIES.get('sel_age')
        odomtr_sel = request.COOKIES.get('sel_odometer')
        fuel_sel = request.COOKIES.get('sel_fuel')
        transm_sel = request.COOKIES.get('sel_transm')
        type_sel = request.COOKIES.get('sel_type')
        color_sel = request.COOKIES.get('sel_color')

        make_index = getAttr(make_sel, 'manufacturer')
        model_index = getAttr(model_sel, 'model')
        fuel_index = getAttr(fuel_sel, 'fuel')
        transmission_index = getAttr(transm_sel, 'transmission')
        type_index = getAttr(type_sel, 'type')
        paint_color_index = getAttr(color_sel, 'paint_color')

        prediction_df = pd.DataFrame(
            columns=['manufacturer', 'model', 'fuel', 'odometer', 'transmission', 'type', 'paint_color', 'age'])
        prediction_df.loc[0] = [make_index, model_index, fuel_index, odomtr_sel, transmission_index, type_index,
                                paint_color_index, age_sel]

        single_car_result = model_joblib.predict(prediction_df)

        form_reslt = "{:,.2f}".format(single_car_result[0])
        prediction = '$' + str(form_reslt)

        # different scoll down command to display the results

        context = {
            'prediction_form_scroll': 'True',
            'form_scroll': '',
            'prediction': prediction

        }
        response = render(request, "car-price-predictor.html", context)

        return response  # show the element now


def no_nan_other(uniq_types):
    """
    This method was formed as a filter. Takes out ``nan`` and ``other`` as selection options.

    :param List uniq_types: Selected attribute
    :return:  **uniq_types** (*List*) - The list with ``nan`` and ``other`` as selection options.
    """
    uniq_types = [i for i in uniq_types if str(i) != 'nan']
    uniq_types = [i for i in uniq_types if str(i) != 'other']
    return uniq_types


