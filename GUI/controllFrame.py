from    Util        import  sortTrJsonDataByElement
import  tkinter     as      tk
from    tkinter     import  ttk
import  random
import  json
import  os

class ControllFrame(ttk.Frame) :
    
    def __init__(self, parent, root, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.root = root
        self.parent = parent

        self["style"] = "ControllFrame.TFrame"

        self.configure(relief="flat", borderwidth=1)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        for columno in range(0, 7) :
            self.columnconfigure(columno, weight=1)

        self.sortCombines = {"Course Code":False, "Course Name":False, "Course Language":False, "Course ETCS":False, "Course Notation":False, "Course Grade":False, "Course Code":False, "Course Date":False}
        self.lastSortCombine = None

        orderSortButton = ttk.Button(self, text="Sort by Date", command=lambda : self._sortData("Course Date"), style="ControllFrameSortButton.TButton")
        courseCodeSortButton = ttk.Button(self, text="Sort by Code", command=lambda : self._sortData("Course Code"), style="ControllFrameSortButton.TButton")
        courseNameSortButton = ttk.Button(self, text="Sort by Name", command=lambda : self._sortData("Course Name"), style="ControllFrameSortButton.TButton")
        courseLanguageSortButton = ttk.Button(self, text="Sort by Language", command=lambda : self._sortData("Course Language"), style="ControllFrameSortButton.TButton")
        courseEtcsSortButton = ttk.Button(self, text="Sort by ETCS", command=lambda : self._sortData("Course ETCS"), style="ControllFrameSortButton.TButton")
        courseNotationSortButton = ttk.Button(self, text="Sort by Notation", command=lambda : self._sortData("Course Notation"), style="ControllFrameSortButton.TButton")
        courseGradeSortButton = ttk.Button(self, text="Sort by Grade", command=lambda : self._sortData("Course Grade"), style="ControllFrameSortButton.TButton")

        orderSortButton.grid(row=0, column=0, sticky="WE")
        courseCodeSortButton.grid(row=0, column=1, sticky="WE")
        courseNameSortButton.grid(row=0, column=2, sticky="WE")
        courseLanguageSortButton.grid(row=0, column=3, sticky="WE")
        courseEtcsSortButton.grid(row=0, column=4, sticky="WE")
        courseNotationSortButton.grid(row=0, column=5, sticky="WE")
        courseGradeSortButton.grid(row=0, column=6, sticky="WE")

        resetButton = ttk.Button(self, text="Reset", command=self._resetData, style="ControllFrameSettButton.TButton")
        magicButton = ttk.Button(self, text="Suprise", command=self._doSomeMagic, style="ControllFrameSettButton.TButton")
        dummy = ttk.Button(self, text="", state="disabled", style="ControllFrameDummyButton.TButton")
        restartButton = ttk.Button(self, text="Restart", command=self.root.restartProgram, style="ControllFrameSettButton.TButton")
        exitButton = ttk.Button(self, text="Exit", command = self.root.destroy, style="ControllFrameSettButton.TButton")

        resetButton.grid(row=1, column=0, columnspan=2, sticky="WE")
        magicButton.grid(row=1, column=2, sticky="WE")
        dummy.grid(row=1, column=3, sticky="WE")
        restartButton.grid(row=1, column=4, sticky="WE")
        exitButton.grid(row=1, column=5, columnspan=2, sticky="WE")

        for label in self.winfo_children():
            label["cursor"] = "hand2"
            label.grid_configure(padx=1)

    def _sortData(self, element, *event) :
        sortTrJsonDataByElement(element, self.sortCombines[element])
        self.sortCombines[element] = not self.sortCombines[element]
        self.lastSortCombine = element
        self._updateData()

    def _resetData(self, *event) :
        self.lastSortCombine = None
        self.root.displaySection.coursesShouldBeHighlighted.clear()
        with open (os.path.abspath("Temp/transcriptDataInit.json"), "r", encoding="utf-8") as f :
            with open (os.path.abspath("Temp/transcriptData.json"), "w", encoding="utf-8") as f2 :
                f2.write(f.read())
        self._updateData()

    def _updateData(self, *event) :
        self.root.displaySection.gridCoursesOnCanvas()

    def _confirmValues(self, *event) :
        self.root.displaySection.updateCGPA()

    # I knew you were wondering wtf was this method doing. It does nothing. It just used to fills the empty spaces ... (sory)
    def _doSomeMagic(self) :
        self.lastSortCombine = None

        luckyNotation = random.choice(self.root.displaySection.possibleNotations[:-3])

        self.root.displaySection.coursesShouldBeHighlighted = [courseCode for courseCode in self.root.displaySection.allCourses]

        with open (os.path.abspath("Temp/transcriptData.json"), "r", encoding="utf-8") as f :
            data = json.load(f)

        for courseValues in data.values() :
            courseValues[-3] = luckyNotation
            try :
                weight = self.root.displaySection.weights[luckyNotation]
            except KeyError :
                weight = 0
            courseValues[-2] = weight * float(courseValues[-4])

        with open (os.path.abspath("Temp/transcriptData.json"), "w", encoding="utf-8") as f :
            json.dump(data, f, indent=4)

        self._updateData()