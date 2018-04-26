from flask import Flask, jsonify, request
from flask_cors import CORS
from pymodm import connect
import datetime
from timeConvert import str2time, time2str
from checkListOfString import check_list_of_string
from check_for_user import Check_For_User
from tmpFolderAction import make_tmp, access_tmp
from base64_conv_numpy import encode_image_string
from base64_conv_numpy import convert_image_to_np_array
from base64_conv_numpy import convert_processed_np_array_to_base64
from histo_equal import histo_equal
from logCompression import logComp
from reverseVideo import reverseVid
from contr_strech import contr_stretch
from create_histo import create_histo
import logging

app = Flask(__name__)
CORS(app)
connect("mongodb://vcm-3594.vm.duke.edu:27017/image_process_app")


@app.route("/", methods=["GET"])
def welcome():
    """ Function that greets the user on the main page!
    """
    return "Welcome to CrunchWrap Pizza Image Processor!"


@app.route("/process", methods=["POST"])
def process():
    """Function that processes the pre-processed image.

    :returns: json with information to display pre- and post- \
            processed images
    """
    logging.basicConfig(filename='back_end.log', format='%(asctime)s \
    %(message)s', datefmt='%m/%d/%Y %I:%M:%S %pi')
    logging.info("Begin app route to /process")
    info = request.get_json()
    # Make sure the json received is correct
    try:
        email = info["user_email"]
    except KeyError:
        return jsonify("no email input"), 400
        print("No email input")
    check_email = Check_For_User(email)
    if check_email.user_exists is False:
        return jsonify(str(email) + " was not found. Please re-enter"), 400
        print(str(email) + " was not found. Please re-enter")
    try:
        pre_img = info["pre_b64_string"]
    except KeyError:
        return jsonify("no pre_image input"), 400
        print("Please provide pre_image base64 string")
    try:
        method = info["proc_method"]
    except KeyError:
        return jsonify("no proc_method input"), 400
        print("no processing method selected")

    try:
        isinstance(email, str)
        check_list_of_string(pre_img)
        isinstance(method, str)
    except TypeError:
        return jsonify("email is not string"), 400
        print("Please provide information in string format!")
    # if cases that will direct to the correct processing method
    # it would be better to import these methods from a separate file
    current_time = datetime.datetime.now()
    processed_list = []   # this is the list of strings of processed images
    processed_histograms = []
    pre_img_list = []
    pre_img_histograms = []
    for i, img in enumerate(pre_img):
        # for loop to go through all images
        # save user image with correct number
        # add method from main.py
        # save_image
        if method == "histeq":
            imgArray, a_type, m, w, z = convert_image_to_np_array(img)
            hist_equal_image = histo_equal(imgArray)
            histogram_of_pre_img = create_histo(imgArray)
            histogram_of_post_img = create_histo(hist_equal_image)
            hist_equal_img64 = convert_processed_np_array_to_base64(hist_equal_image)
            processed_list.append(hist_equal_img64)
            pre_img_list.append(pre_img)
            processed_histograms.append(histogram_of_post_img)
            pre_img_histograms.append(histogram_of_pre_img)
            return_size = (str(m)+str(w) + ' pixels')
            # Add function for histogram equalization
                # input is pre_img (depending on scikit or whatever,
                # may need to convert format then back to a b64 image string)
                # output is post_img
            # post_img = FOOBAR NOW, post_img should be list of strings
            # Once complete, save user action to database
                # remember we need to identify by __id or something
                # instead of adding with just email
                # add_hist from main.py
            # save processed b64 string
                # adds to the list of processed image strings in b64
            processed_list.append(post_img)
            if i == len(pre_img) - 1:  # last image in list
                new_time = datetime.datetime.now()
                duration = new_time - current_time
                new_info = {
                    "user_email": email,
                    "proc_method": method,
                    "pre_b64_string": pre_img_list,
                    "post_b64_string": processed_list,
                    "pre_histogram": pre_img_histograms,
                    "post_histograms": processed_histograms,
                    "action_time": time2str(duration),
                    "upload_time": time2str(current_time)
                    "pic_size": return_size
                }
                # need to add this list into some tmp folder
                # create_tmp function with json
                # input is (processed_list)
                return jsonify(new_info)
        elif method == "stretch":
            imgArray, a_type, m, w, z = convert_image_to_np_array(img)
            hist_equal_image = contr_stretch(imgArray)
            histogram_of_pre_img = create_histo(imgArray)
            histogram_of_post_img = create_histo(hist_equal_image)
            hist_equal_img64 = convert_processed_np_array_to_base64(hist_equal_image)
            processed_list.append(hist_equal_img64)
            pre_img_list.append(pre_img)
            processed_histograms.append(histogram_of_post_img)
            pre_img_histograms.append(histogram_of_pre_img)
            return_size = (str(m)+str(w) + ' pixels')
            # Add function for contrast stretching
            # input is pre_img (depending on scikit or whatever,
                # may need to convert format then back to a b64 image string)
                # output is post_img
            # post_img = FOOBAR NOW, post_img should be list of strings
            # Once complete, save user action to database
                # remember we need to identify by __id or something
                # instead of adding with just email
                # add_hist from main.py
            # save processed b64 string
                # adds to the list of processed image strings in b64
            processed_list.append(post_img)
            if i == len(pre_img) - 1:  # last image in list
                new_time = datetime.datetime.now()
                duration = new_time - current_time
                new_info = {
                    "user_email": email,
                    "proc_method": method,
                    "pre_b64_string": pre_img_list,
                    "post_b64_string": processed_list,
                    "pre_histogram": pre_img_histograms,
                    "post_histograms": processed_histograms,
                    "action_time": time2str(duration),
                    "upload_time": time2str(current_time)
                    "pic_size": return_size
                }
                # need to add this list into some tmp folder
                # create_tmp function with json
                # input is (processed_list)
                return jsonify(new_info)
        elif method == "logcomp":
            imgArray, a_type, m, w, z = convert_image_to_np_array(img)
            hist_equal_image = logComp(imgArray)
            histogram_of_pre_img = create_histo(imgArray)
            histogram_of_post_img = create_histo(hist_equal_image)
            hist_equal_img64 = convert_processed_np_array_to_base64(hist_equal_image)
            processed_list.append(hist_equal_img64)
            pre_img_list.append(pre_img)
            processed_histograms.append(histogram_of_post_img)
            pre_img_histograms.append(histogram_of_pre_img)
            return_size = (str(m)+str(w) + ' pixels')
            # Add function for log compression
            # input is pre_img (depending on scikit or whatever,
                # may need to convert format then back to a b64 image string)
                # output is post_img
            # post_img = FOOBAR NOW, post_img should be list of strings
            # Once complete, save user action to database
                # remember we need to identify by __id or something
                # instead of adding with just email
                # add_hist from main.py
            # save processed b64 string
                # adds to the list of processed image strings in b64
            processed_list.append(post_img)
            if i == len(pre_img) - 1:  # last image in list
                new_time = datetime.datetime.now()
                duration = new_time - current_time
                new_info = {
                    "user_email": email,
                    "proc_method": method,
                    "pre_b64_string": pre_img_list,
                    "post_b64_string": processed_list,
                    "pre_histogram": pre_img_histograms,
                    "post_histograms": processed_histograms,
                    "action_time": time2str(duration),
                    "upload_time": time2str(current_time)
                    "pic_size": return_size
                }
                # need to add this list into some tmp folder
                # create_tmp function with json
                # input is (processed_list)
                return jsonify(new_info)
        elif method == "reverse":
            imgArray, a_type, m, w, z = convert_image_to_np_array(img)
            hist_equal_image = logComp(imgArray)
            histogram_of_pre_img = reverseVid(imgArray)
            histogram_of_post_img = create_histo(hist_equal_image)
            hist_equal_img64 = convert_processed_np_array_to_base64(hist_equal_image)
            processed_list.append(hist_equal_img64)
            pre_img_list.append(pre_img)
            processed_histograms.append(histogram_of_post_img)
            pre_img_histograms.append(histogram_of_pre_img)
            return_size = (str(m)+str(w) + ' pixels')
            # Add function for reverse video
            # input is pre_img (depending on scikit or whatever,
                # may need to convert format then back to a b64 image string)
                # output is post_img
            # post_img = FOOBAR NOW, post_img should be list of strings
            # Once complete, save user action to database
                # remember we need to identify by __id or something
                # instead of adding with just email
                # add_hist from main.py
            # save processed b64 string
                # adds to the list of processed image strings in b64
            processed_list.append(post_img)
            if i == len(pre_img) - 1:  # last image in list
                new_time = datetime.datetime.now()
                duration = new_time - current_time
                logging.info("Create json to be sent to frontend for preview")
                new_info = {
                    "user_email": email,
                    "proc_method": method,
                    "pre_b64_string": pre_img_list,
                    "post_b64_string": processed_list,
                    "pre_histogram": pre_img_histograms,
                    "post_histograms": processed_histograms,
                    "action_time": time2str(duration),
                    "upload_time": time2str(current_time)
                    "pic_size": return_size
                }
                # create_tmp function with json
                make_tmp(new_info)
                # input is (processed_list)
                return jsonify(new_info)


@app.route("/download", process=["GET"])
def download():
    # access tmp folder and output
    output = access_tmp()
    return jsonify(output)
