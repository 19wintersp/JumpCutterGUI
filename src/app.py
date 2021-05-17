import jumpcutter
import os
import tkinter as tk
import tkinter.filedialog as tk_filedialog
import tkinter.messagebox as tk_msgbox

class JcApp:
	def __init__(self):
		self.root = tk.Tk()
		self.root.title("JumpCutter")
		self.root.resizable(False, False)
		self.root.config(pady=0, padx=0)

		self.input_type = tk.IntVar()
		self.input_type.set(0)
		self.input_file = tk.StringVar()
		self.input_filename = tk.StringVar()
		self.youtube_url = tk.StringVar()
		self.jumpcut_silence = tk.IntVar()
		self.silent_speed = tk.StringVar()
		self.sounded_speed = tk.StringVar()
		self.silent_thresh = tk.StringVar()
		self.frame_margin = tk.StringVar()
		self.sample_rate = tk.StringVar()
		self.frame_rate = tk.StringVar()
		self.frame_quality = tk.StringVar()

		self.jumpcut_silence.set(0)
		self.silent_speed.set("5")
		self.sounded_speed.set("1")
		self.reset_params(True)

		input_section = tk.Frame(self.root, padx=8, pady=8)

		input_label = tk.Label(input_section, text="Input", font=("TkHeadingFont"))
		input_label.grid(row=0, column=0, columnspan=2, sticky=tk.W)

		file_radio = tk.Radiobutton(input_section, variable=self.input_type, value=0)
		file_radio.grid(row=1, column=0, sticky=tk.E+tk.W)
		file_label = tk.Label(input_section, text="Choose a file")
		file_label.grid(row=1, column=1, sticky=tk.W)
		file_content = tk.Frame(input_section)
		file_chooser = tk.Button(file_content, text="Open file", command=self.choose_file_input)
		file_chooser.grid(row=0, column=0)
		file_chosen = tk.Label(file_content, textvariable=self.input_filename, anchor=tk.W)
		file_chosen.grid(row=0, column=1)
		file_content.grid(row=2, column=1, sticky=tk.E+tk.W)

		youtube_radio = tk.Radiobutton(input_section, variable=self.input_type, value=1)
		youtube_radio.grid(row=3, column=0, sticky=tk.E+tk.W)
		youtube_label = tk.Label(input_section, text="Download YouTube URL")
		youtube_label.grid(row=3, column=1, sticky=tk.W)
		youtube_input = tk.Entry(input_section, state=tk.DISABLED, textvariable=self.youtube_url)
		youtube_input.grid(row=4, column=1, sticky=tk.E+tk.W)

		file_radio.config(command=lambda: [
			file_chooser.config(state=tk.NORMAL),
			file_chosen.config(state=tk.NORMAL),
			youtube_input.config(state=tk.DISABLED)
		])
		youtube_radio.config(command=lambda: [
			file_chooser.config(state=tk.DISABLED),
			file_chosen.config(state=tk.DISABLED),
			youtube_input.config(state=tk.NORMAL)
		])

		file_label.bind("<Button-1>", lambda _: file_radio.invoke())
		youtube_label.bind("<Button-1>", lambda _: youtube_radio.invoke())
		
		input_section.columnconfigure(1, weight=1)
		input_section.pack(expand=False, fill=tk.X, anchor=tk.W)

		speed_section = tk.Frame(self.root, padx=8, pady=8)

		speed_label = tk.Label(speed_section, text="Speed", font=("TkHeadingFont"))
		speed_label.grid(row=0, column=0, columnspan=2, sticky=tk.W)

		sound_label = tk.Label(speed_section, text="Sounded speed", padx=8)
		sound_label.grid(row=1, column=0, sticky=tk.E)
		sound_input = tk.Entry(speed_section, textvariable=self.sounded_speed)
		sound_input.grid(row=1, column=1, sticky=tk.E+tk.W)

		silent_label = tk.Label(speed_section, text="Silent speed", padx=8)
		silent_label.grid(row=2, column=0, sticky=tk.E)
		silent_input = tk.Entry(speed_section, textvariable=self.silent_speed)
		silent_input.grid(row=2, column=1, sticky=tk.E+tk.W)

		jumpcut_switch = tk.Checkbutton(speed_section, text="Jumpcut silence", variable=self.jumpcut_silence)
		jumpcut_switch.grid(row=3, column=0, columnspan=2, sticky=tk.W)

		jumpcut_switch.config(command=lambda: [
			silent_label.config(state=(tk.DISABLED if self.jumpcut_silence.get() else tk.NORMAL)),
			silent_input.config(state=(tk.DISABLED if self.jumpcut_silence.get() else tk.NORMAL))
		])

		speed_section.columnconfigure(1, weight=1)
		speed_section.pack(expand=False, fill=tk.X, anchor=tk.W)

		advanced_section = tk.Frame(self.root, padx=8, pady=8)

		advanced_label = tk.Label(advanced_section, text="Advanced", font=("TkHeadingFont"))
		advanced_label.grid(row=0, column=0, columnspan=2, sticky=tk.W)

		thresh_label = tk.Label(advanced_section, text="Silent threshold", padx=8)
		thresh_label.grid(row=1, column=0, sticky=tk.E)
		thresh_input = tk.Entry(advanced_section, textvariable=self.silent_thresh)
		thresh_input.grid(row=1, column=1, sticky=tk.E+tk.W)

		margin_label = tk.Label(advanced_section, text="Frame margin", padx=8)
		margin_label.grid(row=2, column=0, sticky=tk.E)
		margin_input = tk.Entry(advanced_section, textvariable=self.frame_margin)
		margin_input.grid(row=2, column=1, sticky=tk.E+tk.W)

		sample_label = tk.Label(advanced_section, text="Sample rate", padx=8)
		sample_label.grid(row=3, column=0, sticky=tk.E)
		sample_input = tk.Entry(advanced_section, textvariable=self.sample_rate)
		sample_input.grid(row=3, column=1, sticky=tk.E+tk.W)

		framer_label = tk.Label(advanced_section, text="Frame rate", padx=8)
		framer_label.grid(row=4, column=0, sticky=tk.E)
		framer_input = tk.Entry(advanced_section, textvariable=self.frame_rate)
		framer_input.grid(row=4, column=1, sticky=tk.E+tk.W)

		frameq_label = tk.Label(advanced_section, text="Frame quality", padx=8)
		frameq_label.grid(row=5, column=0, sticky=tk.E)
		frameq_input = tk.Entry(advanced_section, textvariable=self.frame_quality)
		frameq_input.grid(row=5, column=1, sticky=tk.E+tk.W)

		reset_butt = tk.Button(advanced_section, text="Reset", command=self.reset_params)
		reset_butt.grid(row=6, column=1, sticky=tk.E)

		advanced_section.columnconfigure(1, weight=1)
		advanced_section.pack(expand=False, fill=tk.X, anchor=tk.W)
		advanced_section.pack_forget()

		actions_section = tk.Frame(self.root, padx=8, pady=8)

		run_butt = tk.Button(actions_section, text="Run", command=self.run_jumpcutter)
		run_butt.pack(side=tk.RIGHT)

		advanced_butt = tk.Button(actions_section, text="Advanced")
		advanced_butt.pack(side=tk.RIGHT)

		advanced_close = tk.Button(actions_section, text="Hide advanced")

		actions_section.pack(expand=False, anchor=tk.E)

		advanced_close.config(command=lambda: [
			advanced_section.pack_forget(),
			advanced_butt.pack(side=tk.RIGHT),
			advanced_close.pack_forget()
		])

		advanced_butt.config(command=lambda: [
			advanced_section.pack(expand=False, fill=tk.X, anchor=tk.W),
			advanced_butt.pack_forget(),
			advanced_close.pack(side=tk.RIGHT),
			actions_section.pack_forget(),
			actions_section.pack(expand=False, anchor=tk.E)
		])

		self.root.mainloop()
	
	def reset_params(self, force = False):
		if not force:
			if not tk_msgbox.askokcancel(
				title="Reset parameters",
				message="This action will reset advanced parameters to their defaults. Proceed?"
			):
				return

		self.silent_thresh.set("0.03")
		self.frame_margin.set("1")
		self.sample_rate.set("44100")
		self.frame_rate.set("30")
		self.frame_quality.set("3")
	
	def choose_file_input(self):
		sel_file = tk_filedialog.askopenfilename()
		sel_filename = ""

		if not sel_file:
			sel_file = ""
		else:
			# find the filename part of the path
			if ("/" in sel_file) or ("\\" in sel_file):
				last_sep = sel_file.replace("\\", "/")[::-1].index("/")
				sel_filename = sel_file[::-1][:last_sep][::-1]
			else:
				sel_filename = sel_file

		self.input_file.set(sel_file)
		self.input_filename.set(sel_filename)
	
	def run_jumpcutter(self):
		file = tk_filedialog.asksaveasfilename()

		if not file:
			return

		def check_type(value, vtype, vname):
			try:
				return vtype(value)
			except:
				msg = "%s should be a %s, but was set to %s.\nIt will be ignored." % (vname, vtype.__name__, value)
				tk_msgbox.showwarning(title="Invalid parameter", message=msg)
				return None
		
		if os.path.exists(file):
			os.remove(file)

		options = {
			"url": None, "input_file": None,
			"output_file": file,
			"silent_threshold": check_type(self.silent_thresh.get(), float, "Silent threshold"),
			"sounded_speed": check_type(self.sounded_speed.get(), float, "Sounded speed"),
			"silent_speed": check_type(self.silent_speed.get(), float, "Silent speed"),
			"frame_margin": check_type(self.frame_margin.get(), int, "Frame margin"),
			"sample_rate": check_type(self.sample_rate.get(), int, "Sample rate"),
			"frame_rate": check_type(self.frame_rate.get(), int, "Frame rate"),
			"frame_quality": check_type(self.frame_quality.get(), int, "Frame quality"),
		}

		if self.input_type.get() == 0:
			options["input_file"] = self.input_file.get()
		else:
			options["url"] = self.youtube_url.get()

		args = lambda: None
		for key in options:
			setattr(args, key, options[key])

		try:
			jumpcutter.main(args)
			tk_msgbox.showinfo(title="Done", message=("Rendering complete; output saved to %s." % file))
		except:
			tk_msgbox.showerror(title="Failed", message="JumpCutter failed unexpectedly.")

def main():
	JcApp()

if __name__ == "__main__":
	main()
