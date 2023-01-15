from django.shortcuts import render,HttpResponse
import requests
#video summarizer
from transformers import pipeline
from youtube_transcript_api import YouTubeTranscriptApi

#video to mp3
import moviepy.editor as mp
from moviepy.editor import *
from tkinter.filedialog import *

from IPython.display import YouTubeVideo

#mic to text
import speech_recognition
#text to summary
from heapq import nlargest
import spacy
from spacy.lang.en.stop_words import STOP_WORDS

# import tkinter
# from tkinter import messagebox


def index(request):
   
    return render(request,'index.html')   

def showsummary(request):

        youtube_video=request.POST.get('videourl')
        video_id = youtube_video.split("=")[1]

        YouTubeVideo(video_id)
        transcript= YouTubeTranscriptApi.get_transcript(video_id)
       
        result=""
        for i in transcript:
            result+=' '+i['text']
      
        summarizer=pipeline('summarization')
        num_iters=int(len(result)/1000)
        summarized_text=[]
        for i in range(0,num_iters+1):
            start=0
            start=i*1000
            end=(i+1)*1000
            out=summarizer(result[start:end])
            out=out[0]
            out=out['summary_text']
            summarized_text.append(out)
    
        return render(request,"index.html",{'output':summarized_text})        


def mictotext(request):
    return render(request,'mictotext.html')
    
def mictextgenerate(request):
    UserVoiceRecognizer = speech_recognition.Recognizer()
 
    while(1):
        try:
    
            with speech_recognition.Microphone() as UserVoiceInputSource:
    
                UserVoiceRecognizer.adjust_for_ambient_noise(UserVoiceInputSource, duration=0.5)
    
                # The Program listens to the user voice input.
                UserVoiceInput = UserVoiceRecognizer.listen(UserVoiceInputSource)    
                UserVoiceInput_converted_to_Text = UserVoiceRecognizer.recognize_google(UserVoiceInput)
                UserVoiceInput_converted_to_Text = UserVoiceInput_converted_to_Text.lower()
               
                return render(request,"mictotext.html",{'micoutput':UserVoiceInput_converted_to_Text})  
        
        except KeyboardInterrupt:
            exit(0)
        
        except speech_recognition.UnknownValueError:
            return render(request,"mictotext.html",{'micoutput':"No User Voice detected OR unintelligible noises detected OR the recognized audio cannot be matched to text !!!"})      


def audiosubmitform(request):
    
    # print("hellooooooooooooooooooo")
    vid = request.POST.get('audioinp')
    str = "static"
    vid = str + "/" + vid
    # print(vid)

    mp3file="static/demo.mp3"
    videoclip= mp.VideoFileClip(vid)
    audioclip=videoclip.audio
    audioclip.write_audiofile(mp3file)
    audioclip.close()
    return render(request,"videotomp3.html",{'audiofile':mp3file})  

def videotomp3(request):
    return render(request,'videotomp3.html')
    

        

def textgenerate(request):
        youtube_video=request.POST.get('videotextinp')
   
        video_id = youtube_video.split("=")[1]       
        YouTubeVideo(video_id)
        transcript= YouTubeTranscriptApi.get_transcript(video_id)        
        result=""
        for i in transcript:
            result+=' '+i['text']
        print(result)    
        return render(request,"videototext.html",{'videotext':result}) 
               
    

def videototext(request):
    return render(request,'videototext.html')
    
def texttosummary(request):
     return render(request,'texttosummary.html')

def textsummary(request):      
        from string import punctuation
        text =request.POST.get('textinp');
        stopwords = list(STOP_WORDS)
        # create nlp model
        nlp = spacy.load('en_core_web_sm')
        doc = nlp(text)
        tokens = [token.text for token in doc]
        # print(tokens)  # all words of text printed
        # print(punctuation)  #all punctuations are stored in this like  , . / ! etc
        punctuation = punctuation +'\n'

        #  now text cleaning removing punct , and stop words
        word_frequencies = {}
        for word in doc:
            if word.text.lower() not in stopwords:
                if word.text.lower() not in punctuation:
                    if word.text not in word_frequencies.keys():
                        word_frequencies[word.text]=1  # if seeing word for first time , freq of that word is 1 ,ekse incr freq
                    else:
                        word_frequencies[word.text]  += 1
        # print(word_frequencies)
        max_frequency = max(word_frequencies.values())
        for word in word_frequencies.keys():
            word_frequencies[word] = word_frequencies[word]/max_frequency

        # print(word_frequencies)
        # sentence tokenization, take each sentence till fullstop
        sentence_tokens = [sent for sent in doc.sents]
        # print(sentence_tokens)
        sentence_scores ={}
        for sent in sentence_tokens:
            for word in sent:
                if word.text.lower() in word_frequencies.keys():
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word.text.lower()]
                    else:
                        sentence_scores[sent] += word_frequencies[word.text.lower()]   
        # print(sentence_scores)
        # now we want 30% of text of sentence with max score

        
        select_length = int(len(sentence_tokens)*0.3)
        summary = nlargest(select_length,sentence_scores,key=sentence_scores.get)
        final_summary = [word.text for word in summary]
        summary = ' '. join(final_summary)
    #   print(summary)
        return render(request,"texttosummary.html",{'textsummary':summary}) 