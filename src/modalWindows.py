

import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
import subprocess as sp
import string
import os
import threading
try:
  from .encodingUtils import cleanFilenameForFfmpeg
except:
  from encodingUtils import cleanFilenameForFfmpeg
from datetime import datetime


class YoutubeDLModal(tk.Toplevel):
  
  def __init__(self, master=None,controller=None,initialUrl='', *args):
    tk.Toplevel.__init__(self, master)
    self.grab_set()
    self.title('Download a video with youtube-dlp')
    self.style = ttk.Style()
    self.style.theme_use('clam')
    self.minsize(600,140)
    self.controller=controller

    self.columnconfigure(0, weight=0)    
    self.columnconfigure(1, weight=1)
    
    self.rowconfigure(0, weight=0)
    self.rowconfigure(1, weight=0)
    self.rowconfigure(2, weight=0)

    self.labelUrl = ttk.Label(self)
    self.labelUrl.config(text='Url')
    self.labelUrl.grid(row=0,column=0,sticky='new',padx=5,pady=5)
    self.varUrl   = tk.StringVar(self,initialUrl)
    self.entryUrl = ttk.Entry(self,textvariable=self.varUrl)
    self.entryUrl.grid(row=0,column=1,sticky='new',padx=5,pady=5)

    self.labelPlaylistLimit = ttk.Label(self)
    self.labelPlaylistLimit.config(text='Max download count')
    self.labelPlaylistLimit.grid(row=1,column=0,sticky='new',padx=5,pady=5)
    self.varPlayListLimit   = tk.StringVar(self,'')
    self.entryPlayListLimit = ttk.Entry(self,textvariable=self.varPlayListLimit)
    self.entryPlayListLimit.grid(row=1,column=1,sticky='new',padx=5,pady=5)

    self.labelUsername = ttk.Label(self)
    self.labelUsername.config(text='Username')
    self.labelUsername.grid(row=2,column=0,sticky='new',padx=5,pady=5)
    self.varUsername   = tk.StringVar(self,'')
    self.entryUsername = ttk.Entry(self,textvariable=self.varUsername)
    self.entryUsername.grid(row=2,column=1,sticky='new',padx=5,pady=5)

    self.labelPassword = ttk.Label(self)
    self.labelPassword.config(text='Password')
    self.labelPassword.grid(row=3,column=0,sticky='new',padx=5,pady=5)
    self.varPassword   = tk.StringVar(self,'')
    self.entryPassword = ttk.Entry(self,textvariable=self.varPassword)
    self.entryPassword.grid(row=3,column=1,sticky='new',padx=5,pady=5)

    self.labelCookies = ttk.Label(self)
    self.labelCookies.config(text='Use cookies.txt')
    self.labelCookies.grid(row=4,column=0,sticky='new',padx=5,pady=5)
    
    self.useCookies = tk.IntVar(0)
    self.entryCookies =  ttk.Checkbutton(self,text='Send credentials from cookies.txt',var=self.useCookies)
    if not os.path.exists('cookies.txt'):
      self.entryCookies['state']='disabled'
      self.entryCookies['text']='cookies.txt not found.'

    self.entryCookies.grid(row=4,column=1,sticky='new',padx=5,pady=5)


    self.downloadCmd = ttk.Button(self)
    self.downloadCmd.config(text='Download',command=self.download)
    self.downloadCmd.grid(row=5,column=0,columnspan=2,sticky='nesw')
    self.rowconfigure(5, weight=1)

    self.entryUrl.focus()
    self.entryUrl.select_range(0, 'end')
    self.entryUrl.icursor('end')

  def download(self):
    url=self.varUrl.get()
    fileLimit=0
    username=self.varUsername.get()
    password=self.varPassword.get()
    useCookies = bool(self.useCookies.get())

    try:
      fileLimit = int(float(self.varPlayListLimit.get()))
    except Exception as e:
      print(e)
    self.controller.loadVideoYTdlCallback(url,fileLimit,username,password,useCookies)
    self.destroy()



class PerfectLoopScanModal(tk.Toplevel):
  
  def __init__(self, master=None,useRange=False,controller=None,starttime=0,endtime=0, *args):
    tk.Toplevel.__init__(self, master)
    self.grab_set()
    self.title('Scan for perfect loops')

    self.controller=controller

    self.columnconfigure(0, weight=0)    
    self.columnconfigure(1, weight=1)
    
    self.rowconfigure(0, weight=0)
    self.rowconfigure(1, weight=0)
    self.rowconfigure(2, weight=0)
    self.rowconfigure(3, weight=0)
    self.rowconfigure(4, weight=0)
    self.rowconfigure(5, weight=0)
    self.rowconfigure(6, weight=0)
    self.rowconfigure(7, weight=0)
    

    self.useRange = useRange

    initThreshold    = 20
    initMidThreshold = 20
    initMinLength    = 1.5
    initMaxLength    = 5.5
    initTimeSkip     = 0.5

    r=0
    if self.useRange:

      self.labelStartTime = ttk.Label(self)
      self.labelStartTime.config(text='Scan start timestamp')
      self.labelStartTime.grid(row=r,column=0,sticky='new',padx=5,pady=5)

      self.varStartTime   = tk.StringVar(self,starttime)
      self.entryStartTime = ttk.Entry(self,textvariable=self.varStartTime)
      self.entryStartTime.grid(row=r,column=1,sticky='new',padx=5,pady=5)

      r+=1

      self.labelEndTime = ttk.Label(self)
      self.labelEndTime.config(text='Scan end timestamp')
      self.labelEndTime.grid(row=r,column=0,sticky='new',padx=5,pady=5)

      self.varEndTime   = tk.StringVar(self,endtime)
      self.entryEndTime = ttk.Entry(self,textvariable=self.varEndTime)
      self.entryEndTime.grid(row=r,column=1,sticky='new',padx=5,pady=5)

      r += 1


    self.labelThreshold = ttk.Label(self)
    self.labelThreshold.config(text='Max loop difference threshold')
    self.labelThreshold.grid(row=r,column=0,sticky='new',padx=5,pady=5)

    self.varThreshold   = tk.StringVar(self,initThreshold)
    self.entryThreshold = ttk.Entry(self,textvariable=self.varThreshold)
    self.entryThreshold.grid(row=r,column=1,sticky='new',padx=5,pady=5)

    r += 1

    self.labelMidThreshold = ttk.Label(self)
    self.labelMidThreshold.config(text='Min inbetween threshold')
    self.labelMidThreshold.grid(row=r,column=0,sticky='new',padx=5,pady=5)


    self.varMidThreshold   = tk.StringVar(self,initMidThreshold)
    self.entryMidThreshold = ttk.Entry(self,textvariable=self.varMidThreshold)
    self.entryMidThreshold.grid(row=r,column=1,sticky='new',padx=5,pady=5)

    r += 1

    self.labelMinLength = ttk.Label(self)
    self.labelMinLength.config(text='Min loop length')
    self.labelMinLength.grid(row=r,column=0,sticky='new',padx=5,pady=5)

    self.varMinLength   = tk.StringVar(self,initMinLength)
    self.entryMinLength = ttk.Entry(self,textvariable=self.varMinLength)
    self.entryMinLength.grid(row=r,column=1,sticky='new',padx=5,pady=5)

    r += 1

    self.labelMaxLength = ttk.Label(self)
    self.labelMaxLength.config(text='Max loop length')
    self.labelMaxLength.grid(row=r,column=0,sticky='new',padx=5,pady=5)

    self.varMaxLength   = tk.StringVar(self,initMaxLength)
    self.entryMaxLength = ttk.Entry(self,textvariable=self.varMaxLength)
    self.entryMaxLength.grid(row=r,column=1,sticky='new',padx=5,pady=5)


    r += 1

    self.labelTimeSkip = ttk.Label(self)
    self.labelTimeSkip.config(text='Time to skip between loops')
    self.labelTimeSkip.grid(row=r,column=0,sticky='new',padx=5,pady=5)

    self.varTimeSkip   = tk.StringVar(self,initTimeSkip)
    self.entryTimeSkip = ttk.Entry(self,textvariable=self.varTimeSkip)
    self.entryTimeSkip.grid(row=r,column=1,sticky='new',padx=5,pady=5)

    r += 1

    self.scanCmd = ttk.Button(self)
    self.scanCmd.config(text='Scan for loops',command=self.scanForLoops)
    self.scanCmd.grid(row=r,column=0,columnspan=2,sticky='nesw')
    self.rowconfigure(r, weight=1)

    self.resizable(False, False) 

  def scanForLoops(self):
    threshold = float(self.varThreshold.get())
  
    midThreshold = float(self.varMidThreshold.get())
    minLength = float(self.varMinLength.get())
    maxLength = float(self.varMaxLength.get())
    timeSkip  = float(self.varTimeSkip.get())

    

    useRange=self.useRange
    if self.useRange:
      rangeStart=float(self.varStartTime.get())
      rangeEnd=float(self.varEndTime.get())
    else:
      rangeStart=None
      rangeEnd=None

    self.controller.submitFullLoopSearch(midThreshold=midThreshold,
                                         minLength=minLength,
                                         maxLength=maxLength,
                                         timeSkip=timeSkip,
                                         threshold=threshold,
                                         addCuts=True,
                                         useRange=useRange,
                                         rangeStart=rangeStart,
                                         rangeEnd=rangeEnd)
    self.destroy()


class SubtitleExtractionModal(tk.Toplevel):

  def __init__(self, master=None, *args):
    tk.Toplevel.__init__(self, master)
    self.grab_set()
    self.title('Extract Subtitles')
    self.minsize(600,150)
    


    self.columnconfigure(0, weight=0)    
    self.columnconfigure(1, weight=1)
    
    self.rowconfigure(0, weight=0)
    self.rowconfigure(1, weight=0)
    self.rowconfigure(2, weight=0)
    self.rowconfigure(3, weight=0)
    self.rowconfigure(4, weight=1)
    self.rowconfigure(5, weight=0)
    

    self.labelFilename = ttk.Label(self)
    self.file=''
    self.labelFilename.config(text='Source file')
    self.labelFilename.grid(row=0,column=0,sticky='new',padx=5,pady=5)

    self.varFilename   = tk.StringVar()
    self.varFilename.set('None')
    self.entryFilename = ttk.Button(self)
    self.entryFilename.config(text='File: {}'.format(self.varFilename.get()[-20:]),command=self.selectFile)
    self.entryFilename.grid(row=0,column=1,sticky='new',padx=5,pady=5)

    self.labelStream = ttk.Label(self)
    self.labelStream.config(text='Stream Index')
    self.labelStream.grid(row=1,column=0,sticky='new',padx=5,pady=5)

    self.varStream   = tk.StringVar()
    self.varStream.trace('w',self.streamChanged)
    self.entryStream = ttk.Combobox(self)
    self.entryStream.config(textvariable=self.varStream,state='disabled')
    self.entryStream.config(values=[])
    self.entryStream.grid(row=1,column=1,sticky='new',padx=5,pady=5)

    self.labelOutputName = ttk.Label(self)
    self.labelOutputName.config(text='Output Name:')
    self.labelOutputName.grid(row=2,column=0,sticky='new',padx=5,pady=5)

    self.labelOutputFileName = ttk.Label(self)
    self.labelOutputFileName.config(text='None')
    self.labelOutputFileName.grid(row=2,column=1,sticky='new',padx=5,pady=5)

    self.labelProgress = ttk.Label(self)
    self.labelProgress.config(text='Idle')
    self.labelProgress.grid(row=3,column=0,columnspan=2,sticky='new',padx=5,pady=5)


    self.extractCmd = ttk.Button(self)
    self.extractCmd.config(text='Extract',command=self.extract,state='disabled')
    self.extractCmd.grid(row=4,column=0,columnspan=2,sticky='nesw')


    self.statusProgress = ttk.Progressbar(self)
    self.statusProgress['value'] = 0
    self.statusProgress.grid(row=5,column=0,columnspan=2,sticky='nesw')
    self.statusProgress.config(style="Green.Horizontal.TProgressbar")


    self.resizable(False, False) 

    self.outputFilename=''
    self.streamInd=0
    self.subtitleThread=None
    self.close=False

    self.protocol("WM_DELETE_WINDOW", self.closeThreads)


  def selectFile(self):
    self.file = askopenfilename(multiple=False,filetypes=[('All files','*.*',)])
    subn=0
    self.statusProgress['value']=0
    if os.path.isfile(self.file):
      outs,errs = sp.Popen(['ffmpeg','-i',cleanFilenameForFfmpeg(self.file)],stderr=sp.PIPE).communicate()
      print(outs,errs)
      self.subs=[]
      for line in errs.split(b'\n'):
        if b'Stream #' in line and b'Subtitle' in line:
          self.subs.append( str(subn) +' - ' + line.strip().decode('utf8',errors='ignore'))
          subn+=1

      self.entryStream.config(values=self.subs)
      if len(self.subs)>0:
        self.varStream.set(self.subs[0])
        self.entryStream.config(state='normal')
        self.entryFilename.config(text='File: {}'.format(self.file[-100:]))
      else:
        self.varStream.set('')
        self.entryStream.config(state='disabled')
        self.entryFilename.config(text='File: None')
    else:
        self.varStream.set('')
        self.entryStream.config(state='disabled')      
        self.entryFilename.config(text='File: None')

  def streamChanged(self,*args):
    self.outputFilename=''
    self.statusProgress['value']=0
    if os.path.isfile(self.file) and self.varStream.get().split('-')[0].strip().isdigit():
      self.extractCmd.config(state='normal')
      filename = os.path.split(self.file)[-1]
      filename = os.path.splitext(filename)[0]
      streamName = self.varStream.get().split(':')
      self.streamInd = int(streamName[0].split(' ')[0])
      self.outputFilename = ''.join([x for x in filename+'.subs.'+str(self.streamInd)+'.'+streamName[1]+'.srt' if x in string.ascii_letters+string.digits+'. '])
      self.labelOutputFileName.config(text=self.outputFilename)
    else:
      self.extractCmd.config(state='disabled')
      if len(self.subs)==0:
        self.labelOutputFileName.config(text='No subtitle track found')
      else:
        self.labelOutputFileName.config(text='None')

  def watchsubtitleProgress(self):
    l=b''
    expectedLength=None
    self.statusProgress['value']=0
    while 1:
      c = self.proc.stderr.read(1)
      if self.close:
        break
      if len(c)==0:
        break
      if c in b'\n\r':
        print(l)
        if b'Duration: ' in l and expectedLength is None:
          expectedLength=l.split(b'Duration: ')[1].split(b',')[0]
          expectedLength = datetime.strptime(expectedLength.decode('utf8'),'%H:%M:%S.%f')
          expectedLength = expectedLength.microsecond/1000000 + expectedLength.second + expectedLength.minute*60 + expectedLength.hour*3600
        elif b'time=' in l and expectedLength is not None:
          currentReadPos=l.split(b'time=')[1].split(b' ')[0]
          currentReadPos = datetime.strptime(currentReadPos.decode('utf8'),'%H:%M:%S.%f')
          currentReadPos = currentReadPos.microsecond/1000000 + currentReadPos.second + currentReadPos.minute*60 + currentReadPos.hour*3600
          if not self.close:
            self.statusProgress['value']=(currentReadPos/expectedLength)*100
        self.labelProgress.config(text=l)
        l=b''
      else:
        l+=c
    if not self.close:
      self.statusProgress['value']=100
      self.entryStream.config(state='normal')     
      self.entryFilename.config(state='normal')
      self.extractCmd.config(state='normal')

  def closeThreads(self):
    self.close=True
    substhread = self.subtitleThread
    self.subtitleThread=None
    self.destroy()

  def extract(self):
    self.proc = sp.Popen(['ffmpeg','-y','-i', self.file, '-map', '0:s:{}'.format(self.streamInd), '-vsync', '0', '-an', '-vn' , '-f', 'srt' , self.outputFilename],stderr=sp.PIPE)
    self.subtitleThread = threading.Thread(target=self.watchsubtitleProgress)
    self.subtitleThread.daemon = True
    
    self.entryStream.config(state='disabled')     
    self.entryFilename.config(state='disabled')
    self.extractCmd.config(state='disabled')

    self.subtitleThread.start()


class OptionsDialog(tk.Toplevel):
  def __init__(self, master=None, optionsDict={}, changedProperties={}, changeCallback=None, *args):
    tk.Toplevel.__init__(self, master)
    self.grab_set()
    self.title('Options')
    self.minsize(600,140)
    self.optionsDict=optionsDict
    self.changedProperties=changedProperties
    self.changeCallback=changeCallback
    self.entryMap={}
    self.varMap={}
    self.validatorMap={}
    
    self.columnconfigure(0, weight=0)    
    self.columnconfigure(1, weight=1)

    for i,(k,v) in enumerate(optionsDict.items()):
      print(i,k,v)
      labelValue = ttk.Label(self)
      labelValue.config(text=k)
      labelValue.grid(row=i,column=0,sticky='new',padx=5,pady=5)
      valueVar   = tk.StringVar(self)
      self.varMap[k]=valueVar
      entryValue = ttk.Entry(self,textvariable=self.varMap[k])
    
      okayCommand = self.register(lambda val,t=type(v):self.validateType(t,val))  
      self.validatorMap[k]=okayCommand
      entryValue.config(validate='key',validatecommand=(okayCommand ,'%P'))

      valueVar.set(str(v))
      entryValue.grid(row=i,column=1,sticky='new',padx=5,pady=5)
      self.entryMap[k]=entryValue
      valueVar.set(str(v))
      valueVar.trace('w',lambda *args,k=k:self.valueChanged(k))

    self.saveChanges = ttk.Button(self,text='Save Changes',command=self.saveChanges)
    self.rowconfigure(i+1, weight=1)
    self.saveChanges.grid(row=i+1,column=0,columnspan=2,sticky='nesw')


    self.resizable(False, False) 

  def validateType(self,fieldtype,nextVal):
    if nextVal=='':
      return 1
    try:
      fieldtype(nextVal)
      return 1
    except:
      return 0

  def saveChanges(self):
    print(self.changeCallback,self.changedProperties)
    if self.changeCallback is not None:
      print(self.changedProperties)
      self.changeCallback(self.changedProperties)
    self.destroy()

  def valueChanged(self,valueKey):
    originalValue = self.optionsDict[valueKey]
    try:
      if type(originalValue) == int:
        self.changedProperties[valueKey] = int(self.varMap.get(valueKey).get())
      elif type(originalValue) == float:
        self.changedProperties[valueKey] = float(self.varMap.get(valueKey).get())
      elif type(originalValue) == bool:
        self.changedProperties[valueKey] = bool(self.varMap.get(valueKey).get())
      else:
        self.changedProperties[valueKey] = self.varMap.get(valueKey).get()
    except Exception as e:
      try:
        del self.changedProperties[valueKey]
      except Exception as e:
        print(e)
    print(valueKey)

if __name__ == "__main__":
  app = YoutubeDLModal()
  app.mainloop()