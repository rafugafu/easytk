import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.scrolled import ScrolledText, ScrolledFrame
from tkinter import simpledialog as sd
from tkinter import messagebox as mb
from tkinter import filedialog as fd
from tkinter import font
from tkinter import colorchooser as cc
import os
class win(ttk.Window):
	def __init__(self, style = True, *args, **kwargs):
		if type(style) == str:
			super().__init__(themename = style, **kwargs)
		elif style == True:
			super().__init__(themename = 'pulse', **kwargs)
		else:
			super().__init__(themename = 'clam', **kwargs)
		self.imgs = []
		self.path = os.path.dirname(os.path.abspath(__file__))
	def destroy(self):
		try:
			self.update_idletasks()
		except Exception:
			pass
		try:
			ttk.Style.instance = None
		except Exception:
			pass
		tk.Tk.destroy(self)
	def import_theme(self, path):
		self.style()._s.load_user_themes(path)
	def subwin(self):
		subwin = toplevel(self)
		subwin.exists = True
		subwin.transient(self)
		subwin._map_id = self.bind('<Map>', lambda event: subwin.deiconify())
		subwin._unmap_id = self.bind('<Unmap>', lambda event: subwin.withdraw())
		subwin._parent = self
		return subwin
	def getfonts(self):
		return font.families(self)
	def button(self, master = None, text = '', command = None, image = None, imsize = (10, 10), *args, **kwargs):
		if master == None:
			master = self
		if image == None:
			return ttk.Button(master, text = text, command = command, *args, **kwargs)
		else:
			photo = tk.PhotoImage(file = image)
			photoimage = photo.subsample(imsize[0], imsize[1])
			self.imgs.append(photoimage)
			return ttk.Button(master, text = text, command = command, image = self.imgs[len(self.imgs) - 1], compound = 'left', *args, **kwargs)
	def image(self, image, imsize = (10, 10), master = None):
		if master == None:
			master = self
		photo = tk.PhotoImage(file = image)
		photoimage = photo.subsample(imsize[0], imsize[1])
		self.imgs.append(photoimage)
		return ttk.Label(master, image = self.imgs[len(self.imgs) - 1])
	def selall(self, ans):
		ans.tag_add('sel', '1.0', 'end')
		return 'break'
	def textbox(self, master = None, scrolled = False, *args, **kwargs):
		if master == None:
			master = self
		if scrolled == True:
			ans = ScrolledText(master, *args, **kwargs)
			ans.bind = ans.text.bind
		else:
			ans = tk.Text(master, *args, **kwargs)
		ans.bind('<Control-a>', lambda event: self.selall(ans))
		return ans
	def text(self, master = None, text = '', image = None, imsize = (10, 10), *args, **kwargs):
		if master == None:
			master = self
		if image == None:
			return ttk.Label(master, text = text, *args, **kwargs)
		else:
			photo = tk.PhotoImage(file = image)
			photoimage = photo.subsample(imsize[0], imsize[1])
			self.imgs.append(photoimage)
			return ttk.Label(master, text = text, image = self.imgs[len(self.imgs) - 1], compound = 'left', *args, **kwargs)
	def menu(self, master = None, *args, **kwargs):
		if master == None:
			master = self
		return tk.Menu(master, *args, **kwargs)
	def entry(self, master = None, *args, **kwargs):
		if master == None:
			master = self
		return ttk.Entry(master, *args, **kwargs)
	def tabs(self, master = None, *args, **kwargs):
		if master == None:
			master = self
		return ttk.Notebook(master, *args, **kwargs)
	def frame(self, master = None, scrolled = False, *args, **kwargs):
		if master == None:
			master = self
		if scrolled == True:
			return ScrolledFrame(master, *args, **kwargs)
		else:
			return ttk.Frame(master, *args, **kwargs)
	def style(self, style = None, master = None):
		if style == None:
			return ttk.Style()
		else:
			ttk.Style().theme_use(style)
	def themes(self):
		import importlib
		import ttkbootstrap.themes.user as user_themes
		from ttkbootstrap.style import ThemeDefinition
		importlib.reload(user_themes)
		s = self.style()
		existing = s.theme_names()
		for name, definition in user_themes.USER_THEMES.items():
			if name not in existing:
				s.register_theme(ThemeDefinition(name = name, themetype = definition['type'], colors = definition['colors']))
		return sorted(s.theme_names())
	def slider(self, range_, master = None, *args, **kwargs):
		if master == None:
			master = self
		return ttk.Scale(master, from_ = range_[0], to = range_[1], *args, **kwargs)
	def progressbar(self, master = None, *args, **kwargs):
		if master == None:
			master = self
		return ttk.Progressbar(master, *args, **kwargs)
	def scroll(self, master = None, *args, **kwargs):
		if master == None:
			master = self
		return ttk.Scrollbar(master, *args, **kwargs)
	def error(self, title, message):
		return mb.showerror(title, message)
	def info(self, title, message):
		return mb.showinfo(title, message)
	def warning(self, title, message):
		return mb.showwarning(title, message)
	def ask(self, title, question, options, *args, **kwargs):
		options = tuple(options)
		if options == ('yes', 'no'):
			return mb.askyesno(title, question, *args, **kwargs)
		if options == ('ok', 'cancel'):
			return mb.askokcancel(title, question, *args, **kwargs)
		if options == ('yes', 'no', 'cancel'):
			return mb.askyesnocancel(title, question, *args, **kwargs)
		if options == ('retry', 'cancel'):
			return mb.askretrycancel(title, question, *args, **kwargs)
	def strok(self, ans):
		self.strans = ans
	def askstring(self, title, prompt):
		root = self.subwin()
		root.title(title)
		tf = root.frame()
		tf.grid(padx = 5, pady = 5)
		root.text(text = prompt, master = tf).pack(padx = 5, pady = 5)
		ans_ = root.entry(master = tf)
		ans_.pack(fill = 'x', padx = 5, pady = 5)
		bf = root.frame()
		bf.grid(padx = 5, pady = 5)
		root.button(text = 'Cancel', master = bf, command = lambda: self.strok(None)).pack(side = 'left', padx = 5, pady = 5)
		root.button(text = 'OK', master = bf, command = lambda: self.strok(ans_.get())).pack(side = 'right', padx = 5, pady = 5)
		root.bind('<Return>', lambda event: self.strok(ans_.get()))
		root.sizablefalse()
		root.protocol('WM_DELETE_WINDOW', None)
		while True:
			try:
				self.strans
			except Exception:
				try:
					ans_.focus()
					self.update()
				except Exception:
					pass
			else:
				strans = self.strans
				del self.strans
				root.destroy()
				return strans
	def askcolor(self, *args, **kwargs):
		c = cc.askcolor(*args, **kwargs)
		if c[1]:
			return c[1]
		else:
			return None
	def stringvar(self, master = None, *args, **kwargs):
		if master == None:
			master = self
		return tk.StringVar(master, *args, **kwargs)
	def intvar(self, master = None, *args, **kwargs):
		if master == None:
			master = self
		return tk.IntVar(master, *args, **kwargs)
	def booleanvar(self, master = None, *args, **kwargs):
		if master == None:
			master = self
		return tk.BooleanVar(master, *args, **kwargs)
	def listbox(self, contents = None, master = None, *args, **kwargs):
		if master == None:
			master = self
		l = tk.Listbox(master, *args, **kwargs)
		if contents:
			for x in contents:
				l.insert('end', x)
		return l
	def dropdown(self, stringvar, showdefault, options, master = None, *args, **kwargs):
		if master == None:
			master = self
		command = kwargs.pop('command', None)
		if showdefault not in options:
			options = (showdefault,) + tuple(options)
		ans = ttk.OptionMenu(master, stringvar, showdefault, *options, *args, **kwargs)
		stringvar.set(showdefault)
		if command:
			stringvar.trace_add('write', lambda *a: command(stringvar.get()))
		return ans
	def droptype(self, options, command = None, master = None, *args, **kwargs):
		if master == None:
			master = self
		combobox = ttk.Combobox(master, values = options, *args, **kwargs)
		combobox.bind('<<ComboboxSelected>>', lambda event: command())
		return combobox
	def spinbox(self, range_, master = None, *args, **kwargs):
		if master == None:
			master = self
		return ttk.Spinbox(master, from_ = range_[0], to = range_[1])
	def check(self, master = None, *args, **kwargs):
		if master == None:
			master = self
		return ttk.Checkbutton(master, *args, **kwargs)
	def multiplechoice(self, text, var, master = None, *args, **kwargs):
		if master == None:
			master = self
		return ttk.Radiobutton(master, text = text, variable = var, value = text, *args, **kwargs)
	def seticon(self, image):
		self.iconphoto(False, tk.PhotoImage(file = image))
	def separator(self, master = None, way = 'horizontal', *args, **kwargs):
		if master == None:
			master = self
		return ttk.Separator(master, orient = way, *args, **kwargs)
	def label(self, widget, text, color = 'lightyellow', border = 'raised', master = None):
		if master == None:
			master = self
		s = ttk.Style()
		s.configure('Custom.TLabel', background = color)
		lr = ttk.Label(master, relief = border, text = text, style = 'Custom.TLabel')
		widget.bind('<Enter>', lambda event: [lr.place(x = event.widget.winfo_x() + event.widget.winfo_width() - 20, y = event.widget.winfo_y() + event.widget.winfo_height() - 10), lr.lift()])
		widget.bind('<Leave>', lambda event: lr.place_forget())
	def getdir(self, *args, **kwargs):
		return fd.askdirectory(*args, **kwargs)
	def sizablefalse(self):
		try:
			self.update()
			self.minsize(width = self.getgeo()[0], height = self.getgeo()[1])
			self.maxsize(width = self.getgeo()[0], height = self.getgeo()[1])
		except Exception:
			pass
	def sizabletrue(self):
		try:
			self.update()
			self.minsize(width = 0, height = 0)
			self.maxsize(width = 99999, height = 99999)
		except Exception:
			pass
	def show(self, *args, **kwargs):
		return self.mainloop(*args, **kwargs)
	def gettheme(self):
		return ttk.Style().theme_use()
	def openfile(self, types = ['all']):
		return filedialog(self).openfile(types)
	def savefile(self, types = ['all']):
		return filedialog(self).savefile(types)
	def getgeo(self):
		return [self.winfo_width(), self.winfo_height()]
class filedialog():
	def __init__(self, master):
		self.master = master
		self.done = None
	def lfilter(self, filetype):
		if filetype != 'all':
			self.extension = filetype
			self.files.delete(0, 'end')
			for self._file in sorted(os.listdir()):
				self.fileext = os.path.splitext(self._file)[1].removeprefix('.')
				if os.path.isdir(self._file):
					self.files.insert('end', self._file + '/')
				elif len(self._file.split('.')) > 1 and self.fileext == filetype:
					self.files.insert('end', self._file)
		else:
			self.extension = ''
			self.files.delete(0, 'end')
			try:
				for self._file in sorted(os.listdir()):
					self.fileextfake = self._file.split('.')[1:]
					self.fileext = ''
					for s in self.fileextfake:
						self.fileext += s
					if os.path.isdir(self._file):
						self.files.insert('end', self._file + '/')
					else:
						self.files.insert('end', self._file)
			except Exception as error:
				self.root.error('Error', error)
				self.open_('..')
	def openfile(self, types):
		self.root = self.master.subwin()
		self.root.title('Open file')
		self.ff = self.root.frame()
		self.ff.grid(column = 0, row = 0, padx = 20, pady = 20)
		self.fff = self.root.frame(master = self.ff)
		self.fff.pack(fill = 'both', side = 'bottom')
		self.scroll = self.root.scroll(master = self.fff)
		self.scroll.pack(fill = 'y', side = 'right')
		self.files = self.root.listbox(master = self.fff, width = 100, height = 10, yscrollcommand = self.scroll.set)
		self.files.pack(fill = 'both', side = 'bottom')
		self.files.bind('<ButtonRelease-1>', lambda event: self.highlight())
		self.files.bind('<Double-Button-1>', lambda event: self.open_())
		self.scroll.config(command = self.files.yview)
		self.dirshow = self.root.text(master = self.ff)
		self.dirshow.pack(side = 'top', fill = 'x')
		self.fileentry = self.root.entry(master = self.ff, state = 'disabled')
		self.types = self.root.stringvar(value = types[0])
		self.open_(os.getcwd())
		self.back = self.root.button(master = self.ff, text = '<', command = lambda: self.open_('..'))
		self.back.pack(side = 'left')
		self.root.label(self.back, text = 'Back', master = self.ff)
		self.fileentry.pack(side = 'top', fill = 'x')
		self.root.button(text = 'Cancel', command = self.root.destroy).grid(column = 0, row = 1, sticky = 'w', padx = 20, pady = 20)
		self.root.dropdown(self.types, types[0], types, command = lambda val: [self.lfilter(val)]).grid(column = 0, row = 1, padx = 20, pady = 20)
		self.root.button(text = 'Open', command = lambda: self.open_()).grid(column = 0, row = 1, sticky = 'e', padx = 20, pady = 20)
		self.root.sizablefalse()
		while True:
			if not self.root.exists:
				return self.done
			else:
				self.root.update()
	def savefile(self, types):
		self.root = self.master.subwin()
		self.extension = types[0]
		self.root.title('Save file')
		self.ff = self.root.frame()
		self.root.bind('<Return>', lambda event: self.save())
		self.ff.grid(column = 0, row = 0, padx = 20, pady = 20)
		self.fff = self.root.frame(master = self.ff)
		self.fff.pack(fill = 'both', side = 'bottom')
		self.scroll = self.root.scroll(master = self.fff)
		self.scroll.pack(fill = 'y', side = 'right')
		self.files = self.root.listbox(master = self.fff, width = 100, height = 10, yscrollcommand = self.scroll.set)
		self.files.pack(fill = 'both', side = 'bottom')
		self.files.bind('<ButtonRelease-1>', lambda event: self.highlight())
		self.files.bind('<Double-Button-1>', lambda event: self.save())
		self.scroll.config(command = self.files.yview)
		self.dirshow = self.root.text(master = self.ff)
		self.dirshow.pack(side = 'top', fill = 'x')
		self.fileentry = self.root.entry(master = self.ff)
		self.types = self.root.stringvar(value = types[0])
		self.open_(os.getcwd())
		self.new = self.root.button(master = self.ff, text = '+', command = self.mnd)
		self.root.label(self.new, text = 'New directory', master = self.ff)
		self.new.pack(side = 'left')
		self.back = self.root.button(master = self.ff, text = '<', command = lambda: self.open_('..'))
		self.back.pack(side = 'left')
		self.root.label(self.back, text = 'Back', master = self.ff)
		self.fileentry.pack(side = 'top', fill = 'x')
		self.root.button(text = 'Cancel', command = self.root.destroy).grid(column = 0, row = 1, sticky = 'w', padx = 20, pady = 20)
		self.root.dropdown(self.types, types[0], types, command = lambda val: [self.lfilter(val)]).grid(column = 0, row = 1, padx = 20, pady = 20)
		self.root.button(text = 'Save', command = lambda: self.save()).grid(column = 0, row = 1, sticky = 'e', padx = 20, pady = 20)
		self.root.sizablefalse()
		while True:
			if not self.root.exists:
				return self.done
			else:
				self.root.update()
	def mnd(self):
		nd = self.root.askstring('New dir', '')
		if nd:
			try:
				os.mkdir(nd)
			except Exception as error:
				self.root.error('Error', error)
			else:
				self.open_('.')
	def highlight(self):
		self.fileentry.delete(0, 'end')
		try:
			self.fileentry.insert('end', self.files.get(self.files.curselection()[0]))
		except Exception:
			pass
	def open_(self, dir_ = None):
		if dir_ == None:
			try:
				if self.files.get(self.files.curselection()[0])[-1:] == '/':
					self.open_(self.files.get(self.files.curselection()[0]))
				else:
					self.done = os.path.join(os.getcwd(), self.files.get(self.files.curselection()[0]))
					self.root.destroy()
					return
			except Exception:
				pass
		else:
			os.chdir(dir_)
			self.dirshow.config(text = os.getcwd())
			self.fileentry.delete(0, 'end')
		self.lfilter(self.types.get())
	def save(self):
		if self.extension != '':
			formattedfile = os.path.join(os.path.dirname(self.fileentry.get()), os.path.splitext(os.path.basename(self.fileentry.get()))[0] + '.' + self.extension)
		else:
			formattedfile = self.fileentry.get()
		formattedfile = os.path.join(os.getcwd(), formattedfile)
		if os.path.isdir(self.fileentry.get()):
			self.open_(self.fileentry.get())
		elif self.fileentry.get():
			if os.path.exists(formattedfile):
				if self.root.ask('WARNING', 'A file named "{}" already exists. Do you want to replace it?'.format(formattedfile), ('yes', 'no')):
					self.done = formattedfile
					self.root.destroy()
					return
			else:
				self.done = formattedfile
				self.root.destroy()
				return
class toplevel(tk.Toplevel, win):
	def withdraw(self):
		if self.exists:
			tk.Toplevel.withdraw(self)
	def deiconify(self):
		if self.exists:
			tk.Toplevel.deiconify(self)
	def destroy(self):
		self.exists = False
		try:
			self._parent.unbind('<Map>', self._map_id)
			self._parent.unbind('<Unmap>', self._unmap_id)
		except Exception:
			pass
		tk.Toplevel.destroy(self)