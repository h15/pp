#!/usr/bin/env python

import pygtk
pygtk.require("2.0")

import gtk
import gobject
import os
import re
import sys
from pipes import quote

class XmmsCli:
	""" Class for working with xmms2d via nyxmms2 """
	def __init__(self, app):
		self.app = app
		self.play()
		self.is_play = True
	
	def pp(self, null):
		""" switch pause/play """
		if self.is_play:
			self.is_play = False
			self.app.tray.set_from_stock(gtk.STOCK_MEDIA_PLAY)
			self.pause()
		else:
			self.is_play = True
			self.app.tray.set_from_stock(gtk.STOCK_MEDIA_PAUSE)
			self.play()
	
	def radd(self, path):
		""" Add file or directory into xmms2d """
		self.send("add file://%s" % quote(path) )
		
	def clear(self, null):
		""" Flush xmms2d song-list """
		self.send("clear")
	
	def pause(self):
		""" Pause xmms """
		self.send("pause")
		
	def play(self):
		""" Play xmms """
		self.send("play")
		
	def prev(self, null):
		""" Play previous song """
		self.send("prev")
	
	def next(self, null):
		""" Play next song """
		self.send("next")
	
	def quit(self):
		""" Xmms2d exit """
		self.send("server shutdown")
	
	def seekNext(self):
		self.send('seek +5')
		
	def seekPrev(self):
		self.send('seek -5')
			
	def send(self, msg):
		""" Exec nyxmms2 command """
		print msg
		os.system("nyxmms2 %s" % msg)
		
	

class App:
	"""	Class for drawing primitive GUI	"""
	def __init__(self):
		self.xmms = XmmsCli(self)
		#	make menu
		self.menu = gtk.Menu()
		
		self.menu_quit = gtk.ImageMenuItem(gtk.STOCK_QUIT)
		self.menu_clear = gtk.ImageMenuItem(gtk.STOCK_CLEAR)
		self.menu_open = gtk.ImageMenuItem(gtk.STOCK_ADD)
		self.menu_prev = gtk.ImageMenuItem(gtk.STOCK_MEDIA_PREVIOUS)
		self.menu_next = gtk.ImageMenuItem(gtk.STOCK_MEDIA_NEXT)
		
		
		self.menu_open.connect('activate', self.get)
		self.menu_clear.connect('activate', self.xmms.clear)
		self.menu_quit.connect('activate', self.quit)
		self.menu_prev.connect('activate', self.xmms.prev)
		self.menu_next.connect('activate', self.xmms.next)
		
		
		self.menu.append(self.menu_prev)
		self.menu.append(self.menu_next)
		self.menu.append(self.menu_open)
		self.menu.append(self.menu_clear)
		self.menu.append(self.menu_quit)
		
		#	make tray
		self.tray = gtk.StatusIcon()
		self.tray.set_from_stock(gtk.STOCK_MEDIA_PAUSE)
		self.tray.set_tooltip('Primitive Player')
		
		self.tray.connect('activate', self.xmms.pp)
		self.tray.connect('scroll_event', self.scroll_event)
		self.tray.connect('popup-menu', self.popup, self.menu)
		
		#	init
		self.desktop = gtk.gdk.get_default_root_window()
		
	def scroll_event(self,param2,event):
		""" On Scrolling tray """
		if event.direction == gtk.gdk.SCROLL_UP:
			self.xmms.seekNext()
		
		elif event.direction == gtk.gdk.SCROLL_DOWN:
			self.xmms.seekPrev()
	
	def popup(self, widget, button, time, data = None):
		""" rise on right click """
		if button==3 and data:
			data.show_all()
			data.popup(None, None, None, 3, time)
	
	def get(self, null):
		""" Add directory for playing """
		dialog = gtk.FileChooserDialog( 'Open', None,	\
			gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER,		\
			(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,		\
			gtk.STOCK_OPEN, gtk.RESPONSE_OK))
				
		response = dialog.run()
		if response == gtk.RESPONSE_OK:
			print dialog.get_filename(), 'selected'
		elif response == gtk.RESPONSE_CANCEL:
			print 'No files selected'
		
		self.xmms.radd(dialog.get_filename())

		dialog.destroy()
	
	def quit(self, widget):
		""" Just quit """
		self.xmms.quit()
		gtk.main_quit()

if __name__ == "__main__":
	os.system('xmms2d &')
	app = App()
	gtk.main()
