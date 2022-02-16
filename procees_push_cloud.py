from distutils.command.clean import clean
import numpy as np
from sklearn import preprocessing
import tensorflow as tf
import sys

def clean_voltage(voltage) :
    voltage_data = str(voltage).split('.')
    if len(voltage_data) > 1:
        res = float(voltage_data[0]+"."+voltage_data[1])
    else:
        res = float(voltage_data[0])
    return res

def clean_current(current) :
    current_data = str(current).split('.')
    if len(current_data) > 1:
        res = float(current_data[0]+"."+current_data[1])
    else:
        res = float(current_data[0])
    return res

def clean_realPower(realPower):
    rp_data = str(realPower).split(".")
    if len(rp_data) > 1:
        res = float(rp_data[0]+"."+rp_data[1])
    else:
        res = float(rp_data[0])
    return res

def clean_powerFactor(powerFactor):
    pf_data = str(powerFactor).split(".")
    if len(pf_data) > 1:
        res = float(pf_data[0]+"."+pf_data[1])
    else:
        res = float(pf_data[0])
    return res

def clean_reactive_power(reactivePower):
    rp_data = str(reactivePower).split(".")
    if len(rp_data) > 1:
        res = float(rp_data[0]+"."+rp_data[1])
    else:
        res = float(rp_data[0])
    return res


def clean_frequency(frequency) :
    freq_data = str(frequency).split(".")
    if len(freq_data) > 1:
        res = float(freq_data[0]+"."+freq_data[1])
    else:
        res = float(freq_data[0])
    return res


def process_input(data1) :
    data = data1.split(',')
    X = []
    #X.append(data[0])
    X.append(clean_voltage(data[1]))  
    X.append(clean_current(data[2]))
    X.append(clean_realPower(data[3]))
    X.append(clean_powerFactor(data[4]))
    X.append(data[5])
    X.append(clean_reactive_power(data[6]))
    X.append(clean_frequency(data[7]))
    print(X)
    sys.stdout.flush()
    get_model_result(X)

def get_model_result(X):
    quantile_transformer = preprocessing.QuantileTransformer(random_state=0)
    X = np.array(X)
    X = X.reshape(-1, 1)
    X_tansform = quantile_transformer.fit_transform(X)

    print(X_tansform)
    interpreter = tf.lite.Interpreter(model_path="/home/pi/minion_lab/model.tflite")
    print(interpreter.get_input_details())
    print(interpreter.get_output_details())
    print(interpreter.get_tensor_details())
    interpreter.allocate_tensors()

    # Get input and output tensors.
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    print(input_details)
    sys.stdout.flush()

    # Test the model on input data.
    input_shape = input_details[0]['shape']
    print(input_shape)
    sys.stdout.flush()

    input_data = np.array(X_tansform, dtype=np.float32)
    input_data = np.array(X_tansform.reshape(1,7), dtype=np.float32)

    interpreter.set_tensor(input_details[0]['index'], input_data)

    interpreter.invoke()

    output_data = interpreter.get_tensor(output_details[0]['index'])
    print("Output data :" + str(output_data))
    sys.stdout.flush()
    with open('/home/pi/model_log.txt','a') as fp:
            fp.write(output_data)
