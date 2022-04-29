#!/usr/bin/env python3

import curses
import clipboard

class App:

    def __init__(self):
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        self.stdscr.nodelay(True)
        curses.start_color()
        self.stdscr.clear()
        
        self.clamp = lambda value, maxV, minV: minV if(value < minV) else maxV if(value > maxV) else value 

        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_CYAN)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)


        self.ccindex = 1

        self.winbuffer = {self.stdscr}

    def add_to_buffer(self, win):
        self.winbuffer.update({win})
    

    def render_all(self):
        for w in self.winbuffer:
            w.noutrefresh()

    def create_menu(self, opts, window, optcount, spacing, deltaX):
    
        for key in opts:
            window.addch(5, 0, str(self.ccindex))
            window.addch(6, 0, key)
            window.addstr(7, 0, str(str(self.ccindex) == key)) 
            if str(self.ccindex) == key:
                window.addstr(int((curses.LINES + spacing * optcount) / 2), int((curses.COLS - len(opts[key])) / 2) - deltaX, opts[key], curses.color_pair(2))
            
            else:
                window.addstr(int((curses.LINES + spacing * optcount) / 2), int((curses.COLS - len(opts[key])) / 2) - deltaX, opts[key]) 
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


def main(stdscr):
    app = App()


    opts = {
        "1": "Starten",
        "2": "Letzte Datei",
        "3": "Beenden"
    }
    # MAIN LOOP #
    while True:
        uInput = app.stdscr.getch()
        app.ccindex = app.clamp(app.ccindex, 3, 1) 
        if uInput == curses.KEY_F1:
            break
        elif uInput == curses.KEY_UP:
            app.ccindex -= 1
        elif uInput == curses.KEY_DOWN:
            app.ccindex += 1
        elif uInput == curses.KEY_ENTER or uInput == 10 or uInput == 13:
            selectedOpt = opts[str(app.ccindex)]
            if selectedOpt == "Beenden":
                exit()
            if selectedOpt == "Starten":
                app.fillwin(app.stdscr, ' ')
                app.stdscr.touchwin()
                break
        

        app.new_statusbar()

        app.create_menu(opts, app.stdscr, -1, 4, 20)
        
        app.render_all()
        curses.doupdate()

    app.stdscr.nodelay(False)
    app.render_all()
    curses.doupdate()
    app.stdscr.getch()

if __name__ == '__main__':
    curses.wrapper(main)


    
