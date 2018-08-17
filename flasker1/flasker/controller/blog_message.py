import sys,os
import tensorflow as tf
from flasker import app
from flask import request,render_template,flash,abort,url_for,redirect,session,Flask,g,json
from .Chinese_poem_generator import model as PHmodel
from .Chinese_poem_generator import data as PHdata

def slicer(string_input):
    poem_list = string_input.split('。')

    for sentence in poem_list:
        sentence += "。"

    return poem_list


@app.route('/', methods=['GET', 'POST'])
def compose_page():
    poem_entries = []
    tf.reset_default_graph()
    trainData = PHdata.POEMS(PHdata.trainPoems)
    MCPangHu = PHmodel.MODEL(trainData)
    if request.method == 'POST':
        cangtou = request.form["cangtou"]
        cangtou_len = len(cangtou)
        if (cangtou_len%2==1):
            poem_entries = ["请输入偶数藏头！"]
        elif (cangtou_len%2==0):
            poems = MCPangHu.testHead(cangtou)
            poem_entries = slicer(poems)


    return render_template('compose.html', entries = poem_entries)

@app.route('/map',methods=['GET','POST'])
def map():
    return render_template('map.html')

@app.route('/paint',methods=['GET','POST'])
def paint():
    return render_template('paint.html')
