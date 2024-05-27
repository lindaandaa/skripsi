import threading
from pylsl import resolve_stream,StreamInlet
import mne
import joblib
import socket

import tkinter as tk

class GUI:
    def __init__(self):
        self.inlet = None

        self.type = None

        self.name = None

        # Create the main window
        self.root = tk.Tk()
        self.root.geometry("800x800")
        self.root.title("Config Interface")

        # Initialize type and listbox
        signals = ["EEG", "EMG"]
        ctypes = tk.StringVar(value=signals)
        self.listbox = tk.Listbox(self.root, listvariable=ctypes, height=2)
        self.listbox.bind('<<ListboxSelect>>', self.item_selected)
        self.listbox.pack(padx=10, pady=10)

        # EEG FRAME

        # Create frames for different signal types
        self.eeg_frame = tk.Frame(self.root)
        self.eeg_label = tk.Label(self.eeg_frame, text="EEG Options")

        # New Listbox for headset type
        headset_types = ["Muse2", "BitbrainVersatile32"]
        cheadset_types = tk.StringVar(value=headset_types)
        self.headset = None
        self.info = None
        self.eeg_headset = tk.Listbox(self.eeg_frame, listvariable=cheadset_types, height=2)
        self.eeg_headset.bind('<<ListboxSelect>>',self.CreateEEGMontage)
        self.eeg_headset.grid(row=0,column=1)

        self.eeg_label.grid(row=1,column=0)

        self.buttonResolveStream = tk.Button(self.eeg_frame,text="Resolve Stream",command=threading.Thread(target=self.OpenStream).start)
        self.buttonResolveStream.grid(row=2,column=1)

        self.buttonPreviewStream = tk.Button(self.eeg_frame,text="Preview Stream",command=threading.Thread(target=self.PreviewStream).start)
        self.buttonPreviewStream.grid(row=2,column=2)

        # Filter parameters

        self.Notch_filter = tk.IntVar()
        self.band_freq_low = tk.DoubleVar()
        self.band_freq_high = tk.DoubleVar()

        self.Notch_filter_bool = tk.IntVar()

        self.CheckboxNotch = tk.Checkbutton(self.eeg_frame,text="Notch Filter",variable=self.Notch_filter_bool,command=self.Notch_filter_on)
        self.CheckboxNotch.grid(row=3,column=1)

        self.Band_Freq_bool = tk.IntVar()

        self.CheckboxBandFreq = tk.Checkbutton(self.eeg_frame,text="Band Freq Filter",variable=self.Band_Freq_bool,command=self.Band_Freq_on)
        self.CheckboxBandFreq.grid(row=3,column=3)

        

        # Model loader

        self.fname = tk.StringVar()
        self.model = None

        self.labelFile = tk.Label(self.eeg_frame,text="Path to the model")
        self.labelFile.grid(row=4,column=0)

        self.filename = tk.Entry(self.eeg_frame,textvariable=self.fname)
        self.filename.grid(row=4,column=1)

        self.buttonLoadModel = tk.Button(self.eeg_frame,text='Load Model',command=threading.Thread(target=self.LoadModel).start)
        self.buttonLoadModel.grid(row=4,column=2)


        # Epoch Setting

        self.Epoch_time = tk.DoubleVar()

        self.labelEpoch = tk.Label(self.eeg_frame,text="Epoch duration")
        self.labelEpoch.grid(row=5,column=0)

        self.entryEpoch = tk.Entry(self.eeg_frame,textvariable=self.Epoch_time)
        self.entryEpoch.grid(row=5,column=1)

        #Launch Server 

        self.buttonLaunchEEG = tk.Button(self.eeg_frame,text="Launch Server",command=threading.Thread(target=self.LaunchServer).start)
        self.buttonLaunchEEG.grid(row=6,column=1)

        # EMG FRAME

        self.emg_frame = tk.Frame(self.root)
        self.emg_label = tk.Label(self.emg_frame, text="EMG Options")
        self.emg_label.grid(row=1,column=0,padx=10)

        self.emg_info_console = tk.Text(self.emg_frame,wrap='word')
        self.emg_info_console.config(state='disabled')
        self.emg_info_console.grid(row=2,column=4,padx=10,columnspan=3,rowspan=3)

        self.buttonResolveStream = tk.Button(self.emg_frame,text="Resolve Stream",command=threading.Thread(target=self.OpenStreamEMG).start)
        self.buttonResolveStream.grid(row=2,column=1,padx=10)

        self.buttonPreviewEMG = tk.Button(self.emg_frame,text="Preview Stream",command=threading.Thread(target=self.PreviewEMG).start)
        self.buttonPreviewEMG.grid(row=2,column=2,padx=10)

        self.calibration_value = 0.0

        self.buttonCalibration = tk.Button(self.emg_frame,text="Calibration",command=threading.Thread(target=self.Calibration).start)
        self.buttonCalibration.grid(row=3,column=1,padx=10)

        self.calibrationRatioLabel = tk.Label(self.emg_frame,text="Ration to Max value to send : ")
        self.calibrationRatioLabel.grid(row=3,column=2,padx=10,pady=5)

        self.Ratio = tk.DoubleVar()

        self.RatioEntry = tk.Entry(self.emg_frame,textvariable=self.Ratio)
        self.RatioEntry.grid(row=3,column=3,padx=10,pady=5)

        self.buttonLaunchEMG = tk.Button(self.emg_frame,text="Launch Server",command=threading.Thread(target=self.LaunchEMG).start)
        self.buttonLaunchEMG.grid(row=4,column=1,padx=10,pady=5,rowspan=3)

        # Placeholder for the label that will display the resolved stream information
        self.label_resolve_stream = tk.Label(self.root, text="Resolving Stream for info:")
        self.label_resolve_stream.pack()

    def item_selected(self, event):
        # Get the selected type
        selected_id = self.listbox.curselection()
        self.type = self.listbox.get(selected_id)

        # Store the current selection in the Listbox
        current_selection = None
        if self.type == "EEG":
            current_selection = self.eeg_headset

        # Set the selection in the current Listbox
        if current_selection:
            current_selection.select_set(0)  # Assumes you want the first item to be selected

        # Hide all frames initially
        self.eeg_frame.pack_forget()
        self.emg_frame.pack_forget()

        # Show the frame based on the selected type
        if self.type == "EEG":
            self.eeg_frame.pack()
            self.type = 'type'
            self.name = 'EEG'
            self.eeg_info_label = tk.Text(self.eeg_frame,wrap="word")
            self.eeg_info_label.grid(row=0,column=3)
        elif self.type == "EMG":
            self.emg_frame.pack()
            self.type = 'name'
            self.name = 'OpenSignals'

    def OpenStream(self):
        os_stream = resolve_stream(self.type,self.name)
        self.inlet = StreamInlet(os_stream[0])
        text = "\n"+"Inlet Created"
        self.eeg_info_label.config(state='normal')
        self.eeg_info_label.insert(tk.END,text)
        self.eeg_info_label.config(state='disabled')

    def OpenStreamEMG(self):
        os_stream = resolve_stream(self.type,self.name)
        self.inlet = StreamInlet(os_stream[0])
        text = "\n"+"Inlet Created"
        self.emg_info_console.config(state='normal')
        self.emg_info_console.insert(tk.END,text)
        self.emg_info_console.config(state='disabled')

    def CreateEEGMontage(self, event):
        eeg_selected_id = self.eeg_headset.curselection()
        self.headset = self.eeg_headset.get(eeg_selected_id)

        if self.headset == "Muse2":
            self.number_channels = 5
            sfreq = 256
            chnames = ['TP9','AF7','AF8','TP10','Right AUX']
            chtypes = ['eeg'] * 4 + ['misc']
            self.info = mne.create_info(chnames,sfreq,chtypes)
        elif self.headset == "BitbrainVersatile32":
            self.number_channels = 32
            sfreq = 256
            chnames = ['Fp1','Fpz','Fp2','AF3','AF4','F7','F3','Fz','F4','F8','FC5','FC1','FC2','FC6','T3','C3','Cz','C4','T4','CP5','CP1','CP2','CP6','T5','P3','Pz','P4','T6','POz','O1','Oz','O2']
            chtypes = ['eeg'] * 32
            self.info = mne.create_info(chnames,sfreq,chtypes)
            self.info.set_montage('standard_1020')

        self.eeg_info_label.config(state='normal')
        self.eeg_info_label.delete(1.0,tk.END)
        text = "List of channels : "
        for i in self.info.ch_names:
            text += i + " "
        self.eeg_info_label.insert(tk.END,text)
        self.eeg_info_label.config(state='disabled')
    
    def PreviewStream(self):
        data = []
        n = 0
        while n < 256:
            sample,timestamp = self.inlet.pull_sample()
            data.append(sample)
            n+=1
        if self.number_channels == 32:
            organised_data = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
        elif self.number_channels == 5:
            organised_data = [[],[],[],[],[]]
        for i in range(len(data)):
            for j in range(len(organised_data)):
                organised_data[j].append(data[i][j])
        raw = mne.io.RawArray(organised_data,self.info)
        self.eeg_info_label.config(state='normal')
        text = "\n"+"One second preview"+"\n"
        self.eeg_info_label.insert(tk.END,text)
        self.eeg_info_label.insert(tk.END,raw.to_data_frame())
        self.eeg_info_label.config(state='disabled')
    
    def LoadModel(self):
        self.model = joblib.load(self.fname.get())
        self.eeg_info_label.config(state='normal')
        text = "\n"+"Model Loaded"
        self.eeg_info_label.insert(tk.END,text)
        self.eeg_info_label.config(state='disabled')

    def Notch_filter_on(self):
        if self.Notch_filter_bool.get() == 1:
            self.Notch_filter_value = tk.Entry(self.eeg_frame,textvariable=self.Notch_filter)
            self.Notch_filter_value.grid(row=3,column=2)
            if self.Notch_filter.get() != 0:
                self.eeg_info_label.config(state='normal')
                text="\n"+"Notch Filter set at "+str(self.Notch_filter.get())+" Hz"
                self.eeg_info_label.insert(tk.END,text)
                self.eeg_info_label.config(state='disabled')

    def Band_Freq_on(self):
        if self.Band_Freq_bool.get() == 1:
            self.Band_Freq_value_low = tk.Entry(self.eeg_frame,textvariable=self.band_freq_low)
            self.Band_Freq_value_low.grid(row=4,column=3)
            self.Band_Freq_value_high = tk.Entry(self.eeg_frame,textvariable=self.band_freq_high)
            self.Band_Freq_value_high.grid(row=4,column=4)
            if self.band_freq_low.get() != 0.0 & self.band_freq_high.get() != 0.0:
                self.eeg_info_label.config(state='normal')
                text="\n"+"Band Freq Filter set between "+str(self.band_freq_low.get())+" Hz and "+str(self.band_freq_high.get())+" Hz"
                self.eeg_info_label.insert(tk.END,text)
                self.eeg_info_label.config(state='disabled')

    def LaunchServer(self):
        self.eeg_info_label.config(state='normal')
        text="\n"+"Server Started"
        self.eeg_info_label.insert(tk.END,text)
        self.eeg_info_label.config(state='disabled')
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        server_socket.bind(('localhost', 12345))
        
        server_socket.listen(1)

        while True:
            client_socket, addr = server_socket.accept()
            self.eeg_info_label.config(state='normal')
            text="\n"+"New connection"
            self.eeg_info_label.insert(tk.END,text)
            self.eeg_info_label.config(state='disabled')

            while True:

                try:
                    output = self.RunModel(self)
                    message = str(output)
                    self.eeg_info_label.config(state='normal')
                    text=message+", "
                    self.eeg_info_label.insert(tk.END,text)
                    self.eeg_info_label.config(state='disabled')
                    client_socket.send(bytes(message+",", "utf-8"))
                except:
                    break  

            client_socket.close()

    def RunModel(self):
        data = []
        n = 0
        while n < 256*round(self.Epoch_time.get())+1:
            sample,timestamp = self.inlet.pull_sample()
            data.append(sample)
            n+=1
        if self.number_channels == 32:
            organised_data = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
        elif self.number_channels == 5:
            organised_data = [[],[],[],[],[]]
        for i in range(len(data)):
            for j in range(len(organised_data)):
                organised_data[j].append(data[i][j])
        raw = mne.io.RawArray(organised_data,self.info)
        if self.Notch_filter.get() != 0:
            raw.notch_filter(freqs=self.Notch_filter.get())
        if self.band_freq_high.get() != 0.0 & self.band_freq_low.get() != 0.0:
            raw.filter(l_freq = self.band_freq_low.get(), h_freq = self.band_freq_high.get())
        epoch = mne.make_fixed_length_epochs(raw,duration=self.Epoch_time.get())
        X = epoch.get_data()
        output = self.model.predict(X)
        return output
    
    def PreviewEMG(self):
        self.emg_info_console.config(state='normal')
        text = "\nOne second of Preview : "
        self.emg_info_console.insert(tk.END,text)
        self.emg_info_console.config(state='disabled')
        n=0
        data = []
        while n < 100:
            sample,timestamp = self.inlet.pull_sample()
            data.append(sample[1])
            n+=1
        self.emg_info_console.config(state='normal')
        self.emg_info_console.insert(tk.END,data)
        self.emg_info_console.config(state='disabled')

    def Calibration(self):
        self.emg_info_console.config(state='normal')
        text = "\nLauching Calibration ..."
        self.emg_info_console.insert(tk.END,text)
        self.emg_info_console.config(state='disabled')
        n=0
        data=[]
        while n < 500:
            sample,timestamp = self.inlet.pull_sample()
            data.append(sample[1])
            n+=1
        self.calibration_value = max(data)
        self.emg_info_console.config(state='normal')
        text = " Done ! Calibration value = "+str(self.calibration_value)
        self.emg_info_console.insert(tk.END,text)
        self.emg_info_console.config(state='disabled')
        
    
    def LaunchEMG(self):
        self.emg_info_console.config(state='normal')
        text = "\nServer Started"
        self.emg_info_console.insert(tk.END,text)
        self.emg_info_console.config(state='disabled')
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        server_socket.bind(('localhost', 12345))
        
        server_socket.listen(1)

        while True:

            client_socket, addr = server_socket.accept()
            self.emg_info_console.config(state='normal')
            text = "\nNew connexion\n"
            self.emg_info_console.insert(tk.END,text)
            self.emg_info_console.config(state='disabled')

            while True:

                try:
                    n=0
                    data = []
                    while n < 10:
                        sample,timestamp = self.inlet.pull_sample()
                        data.append(sample[1])
                        n+=1
                    output = max(data)
                    if output < self.calibration_value * self.Ratio.get():
                        output=0
                    message = str(output)
                    self.emg_info_console.config(state='normal')
                    text = message+", "
                    self.emg_info_console.insert(tk.END,text)
                    self.emg_info_console.config(state='disabled')
                    client_socket.send(bytes(message+",", "utf-8"))
                except:
                    break  

            client_socket.close()


# Create an instance of the GUI class
app = GUI()

# Start the Tkinter event loop
app.root.mainloop()
