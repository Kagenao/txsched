#!/usr/bin/env python3

import curses
import clipboard
import art
import datetime


class App:

    global winbuffer
    def __init__(self):
        curses.initscr()
        self.main_window = self.new_main_window()
        curses.noecho()
        curses.raw()
        curses.curs_set(0)
        self.main_window.nodelay(True)
        curses.start_color()
        self.main_window.clear()
        self.ascArtLineLength = 0
        
        self.winbuffer = {self.main_window}


        self.clamp = lambda value, maxV, minV: minV if(value < minV) else maxV if(value > maxV) else value 

        curses.init_color(curses.COLOR_YELLOW, 200, 174, 77)

        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_CYAN)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_CYAN , curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)

        self.ccindex = 1

    def add_to_buffer(self, win):
        self.winbuffer.update({win})

    def render_all(self):
        for w in self.winbuffer:
            w.noutrefresh()

    def new_main_window(self):
        main_window = curses.newwin(curses.LINES - 1, curses.COLS, 1, 0)
        return main_window

    def create_menu(self, opts, window, optcount, spacing, deltaX):

        for key in opts:

            if str(self.ccindex) == key:
                window.addstr(int((curses.LINES + spacing * optcount) / 2), int((curses.COLS - len(opts[key])) / 2) - deltaX, opts[key].upper(), curses.color_pair(2) | curses.A_BOLD)

            else:
                window.addstr(int((curses.LINES + spacing * optcount) / 2), int((curses.COLS - len(opts[key])) / 2) - deltaX, opts[key].upper(), curses.A_BOLD) 
            # window.getch()
            optcount += 1

    def fillwin(self, w, c):
        y, x = w.getmaxyx()
        s = c * (x - 1)
        for l in range(y):
            w.addstr(l, 0, s)
    
    def new_statusbar(self):

        self.statusbar = curses.newwin(1, curses.COLS, 0, 0)
        self.add_to_buffer(self.statusbar)
        self.statusbar.bkgd(' ', curses.color_pair(1) | curses.A_BOLD)
        self.statusbar.addstr(0, 1, "Fr. 29.04.2022")

    def new_quoteWindow(self):

        self.quotewindow = curses.newwin(4, int((curses.COLS / 3)), int((curses.LINES + 10) / 2), int(curses.COLS - (curses.COLS / 4) - (curses.COLS / 3) / 2))
        self.add_to_buffer(self.quotewindow)
        self.quotewindow.bkgd(' ', curses.color_pair(3))
        quote = "Zu wissen bedeutet nicht, nicht zu vergessen."
        author = "~ Bach, Victoria"
        self.quotewindow.addstr(1, 1, quote)
        self.quotewindow.addstr(2, 1, author)
        self.quotewindow.box()

    def ask_filename(self):
        # TODO: ab hier weitermachen, getch() input aneinander hängen um filename von USER zu kriegen

        pass 

def main(stdscr):
    stdscr.nodelay(True)
    app = App()
    
    # TODO: Tagesnamen auf Deutsch übersetzen
    dayAscii = art.text2art(datetime.datetime.now().strftime("%A"))
    
    sA = dayAscii.splitlines()
    count = 0
    app.main_window.attron(curses.color_pair(4) | curses.A_BOLD)
    for line in sA:
        ascArtLineLength = len(line) 
        app.main_window.addstr(int((curses.LINES - 16 + (1 * count)) / 2), int(curses.COLS - (curses.COLS / 4) - (len(line) / 2)), line)
        count += 2
    app.main_window.attroff(curses.color_pair(4) | curses.A_BOLD)

    opts = {
        "1": "Neue Datei",
        "2": "Letzte Datei",
        "3": "Ende"
    }

    app.main_window.refresh()
    app.new_statusbar() # TODO: Uhrzeit oben Rechts, Filename in Mitte, yeah
    app.new_quoteWindow()

    # MAIN LOOP #
    while True:
        uInput = stdscr.getch()
        app.ccindex = app.clamp(app.ccindex, 3, 1)
        if uInput == curses.KEY_F1:
            break
        elif uInput == curses.KEY_UP:
            app.ccindex -= 1
        elif uInput == curses.KEY_DOWN:
            app.ccindex += 1
        elif uInput == curses.KEY_ENTER or uInput == 10 or uInput == 13:
            selectedOpt = opts[str(app.ccindex)]
            if selectedOpt == opts["3"]:
                exit()
            if selectedOpt == opts["1"]:
                app.main_window.erase()
                break
        

        app.create_menu(opts, app.main_window, -1, 6, 50)
        app.render_all()
        curses.doupdate()
        
    app.main_window.nodelay(False)
    app.render_all()
    curses.doupdate()
    app.main_window.getch()



if __name__ == '__main__':

    curses.wrapper(main)
