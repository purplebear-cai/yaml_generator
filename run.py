from flask import Flask
from flask import render_template, request
from flask_cors import CORS, cross_origin
from flaskext.markdown import Markdown

app = Flask(__name__)
app = Flask(__name__)
Markdown(app)
CORS(app, support_credentials=True, resources={r"/*": {"origins": "*"}})
app.config["CORS_HEADERS"] = "Content-Type"
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":

        print(request.form)
        print("")
        print("")
        print("")
        projectName = request.form["projectName"]

        # collect meta configurations
        meta_configurations = get_meta_configurations(request.form)
        print(meta_configurations)

        # collect data configuration
        data_configurations = get_data_configurations(request.form)
        print(data_configurations)

        # collect preprocessor configurations
        preprocessor_configurations = get_preprocessor_configurations(request.form)
        print(preprocessor_configurations)

        # classifier algorithm configurations
        classifier_configurations = get_classifier_configurations(request.form)
        print(classifier_configurations)
        
    return render_template("index.html")


def get_meta_configurations(request_form):
    meta_configurations = {
        "trainPath": request_form["trainPath"],
        "testPath": request_form["testPath"],
        "randomState": request_form["randomState"],
        "testRatio": request_form["testRatio"],
        "kFold": request_form["kFold"]
    }
    return meta_configurations
    
def get_data_configurations(request_form):
    data_configurations = {
        "textCol": request_form["textCol"], 
        "labelCol": request_form["labelCol"], 
        "labels": [x.strip() for x in request_form["labels"].split(",")]
    }
    return data_configurations

def get_preprocessor_configurations(request_form):
    preprocessors = dict()
    
    if "lowercaseName" in request_form and request_form["lowercaseName"]:
        preprocessor_details = {
            "name": request_form["lowercaseName"], 
            "input": request_form["lowercaseInput"], 
            "output": request_form["lowercaseOutput"]
        }
        preprocessors["lowercase_preprocessor"] = preprocessor_details

    if "tokenizerName" in request_form and request_form["tokenizerName"]:
        preprocessor_details = {
            "name": request_form["tokenizerName"], 
            "input": request_form["tokenizerInput"], 
            "output": request_form["tokenizerOutput"]
        }
        preprocessors["tokenizer_preprocessor"] = preprocessor_details
    return preprocessors

def get_classifier_configurations(request_form):
    classifiers = dict()
    
    if "logisticregInput" in request_form and request_form["logisticregInput"]:
        classifier_details = {
            "input": request_form["logisticregInput"],
            "output": request_form["logisticregOutput"],
            "parameters": request_form["logisticregParams"] # TODO
        }
        classifiers["logisticregClassifier"] = classifier_details

    if "huggingfaceInput" in request_form and request_form["huggingfaceInput"]:
        classifier_details = {
            "input": request_form["huggingfaceInput"],
            "output": request_form["huggingfaceOutput"],
            "parameters": request_form["huggingfaceParams"], # TODO, 
            "huggingface_model_name": request_form["huggingfaceModelName"]
        }
        classifiers["huggingfaceClassifier"] = classifier_details

    return classifiers

if __name__ == '__main__':
    # app.jinja_env.auto_reload = True
    # app.config['TEMPLATES_AUTO_RELOAD'] = True
    # app.run(debug=True, host='0.0.0.0')
    app.run(debug=True)