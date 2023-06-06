from    Environment     import  ASSETS_DC, GUI_DC, to_turkish # -> Environment variables
from    tkinter         import  messagebox # -> Interract with user
import  customtkinter   as      ctk # -> GUI

class FilterSelecter(ctk.CTkToplevel) :

    def __init__(self, master : ctk.CTkFrame, filtering : list, available_filterings : list, available_filterings_text_display : str, parsing_language : str) -> None:
        """
        Constructor method for FilterSelecter class. This class is used to select filters.
        @Parameters:
            master - Required : Parent widget of this class. (ttk.Frame) -> Which is the main window.
            filtering - Required : Current filtering. (list) -> List of dict filters.
            available_filterings - Required : Available filterings. (list) -> List of dict available filterings.
            available_filterings_text_display - Required : Available filterings text display. (str) -> Text to display for available filterings.
            parsing_language - Required : Parsing language. (str) -> "tr" or "en"
        @Returns:
            None
        """
        # Initialize the Toplevel class.
        super().__init__(master)
        self.grid_rowconfigure((0), weight=1)
        self.grid_columnconfigure((0), weight=1)

        # Set program language
        self.parsing_language = parsing_language
        
        # Set the title and the icon.
        self.title(self._get_text("Filter Courses"))
        self.iconbitmap(ASSETS_DC.ICON)
        
        # Set class variables
        self.available_filterings_text_display = available_filterings_text_display
        self.available_filterings_show_display = {value: key for key, value in available_filterings_text_display.items()}
        self.available_filterings = available_filterings
        self.current_filtering = filtering.copy()
        self.result = filtering.copy()

        # Create the main container
        self.container = ctk.CTkFrame(self, fg_color=GUI_DC.DARK_BACKGROUND, bg_color=GUI_DC.DARK_BACKGROUND)
        self.container.grid(row=0, column=0, sticky="nsew")
        # Configure the main container
        self.container.grid_rowconfigure((0), weight=1)
        self.container.grid_columnconfigure((0), weight=1)

        # Add an handler on close, for making sure correct data is returned.
        self.protocol("WM_DELETE_WINDOW", self.__clean_exit)
        
        # Create the widgets.
        self.create_widgets()

        # Follow the main window.
        self.grab_set()
        self.focus_set()
        self.wait_window()

    def _get_text(self, text : str) -> str:
        """
        Gets the text from the language dictionary.
        @Parameters:
            text - Required : Text to get from the dictionary. (str) -> Which is used to get the text from the language dictionary for translation.
        @Return:
            translated_text - str : Translated text. (str)
        """
        # According to the language, do the translation.
        if self.parsing_language == "tr" :
            return to_turkish[text]
        else :
            return text

    def create_widgets(self) -> None:
        """
        Creates the widgets.
        @Parameters:
            None
        @Returns:
            None
        """
        # Set the main container.
        self.widgets_container = ctk.CTkFrame(self.container, fg_color=GUI_DC.DARK_BACKGROUND, bg_color=GUI_DC.DARK_BACKGROUND)
        self.widgets_container.grid(row=0, column=0, sticky="nsew")
        # Configure the main container.
        self.widgets_container.grid_rowconfigure((0,1,2), weight=1)
        self.widgets_container.grid_columnconfigure((0,1), weight=1)

        # Create the widgets.
        self.info_label = ctk.CTkLabel(self.widgets_container, text=self._get_text("Select and Remove filters"),
            fg_color=GUI_DC.DARK_BACKGROUND,
            bg_color=GUI_DC.DARK_BACKGROUND,
            text_color=GUI_DC.LIGHT_TEXT_COLOR,
            font=("Arial", 15, "bold"),
            anchor="center",
        )
        self.info_label.grid(row=0, column=0, columnspan=2)

        self.filter_change_container = ctk.CTkFrame(self.widgets_container, fg_color=GUI_DC.DARK_BACKGROUND, bg_color=GUI_DC.DARK_BACKGROUND)
        self.filter_change_container.grid(row=1, column=0, columnspan=2, padx=GUI_DC.INNER_PADDING, pady=GUI_DC.INNER_PADDING)
        self._init_filters()

        self.save_button = ctk.CTkButton(self.widgets_container, text=self._get_text("Apply"), command=self.__save,
            fg_color=GUI_DC.LIGHT_BACKGROUND,
            bg_color=GUI_DC.DARK_BACKGROUND,
            hover_color=GUI_DC.SECONDARY_LIGHT_BACKGROUND,
            text_color=GUI_DC.DARK_TEXT_COLOR,
            text_color_disabled=GUI_DC.MEDIUM_TEXT_COLOR,
            anchor="center",
            font=("Arial", 12, "bold")
        )
        self.save_button.grid(row=2, column=0, pady=GUI_DC.INNER_PADDING, padx=GUI_DC.INNER_PADDING)

        self.cancel_button = ctk.CTkButton(self.widgets_container, text=self._get_text("Cancel"), command=self.__clean_exit,
            fg_color=GUI_DC.LIGHT_BACKGROUND,
            bg_color=GUI_DC.DARK_BACKGROUND,
            hover_color=GUI_DC.SECONDARY_LIGHT_BACKGROUND,
            text_color=GUI_DC.DARK_TEXT_COLOR,
            text_color_disabled=GUI_DC.MEDIUM_TEXT_COLOR,
            anchor="center",
            font=("Arial", 12, "bold")
        )
        self.cancel_button.grid(row=2, column=1, pady=GUI_DC.INNER_PADDING, padx=GUI_DC.INNER_PADDING)

    def _init_filters(self) -> None:
        """
        Initializes the filters.
        @Parameters:
            None
        @Returns:
            None
        """
        # Set the feature variables
        self.row_count = 1 + len(self.current_filtering) + 1 # -> 1 name, n filters, 1 combobox
        # Configure the filtering change container || The row config is scaled according to the number of filters.
        self.filter_change_container.grid_rowconfigure(tuple(range(self.row_count)), weight=1)
        self.filter_change_container.grid_columnconfigure((0, 1, 2), weight=1)

        # Load info labels for operations.
        self.filter_by_label = ctk.CTkLabel(self.filter_change_container, text=self._get_text("Filter By"),
            fg_color=GUI_DC.DARK_BACKGROUND,
            bg_color=GUI_DC.DARK_BACKGROUND,
            text_color=GUI_DC.LIGHT_TEXT_COLOR,
            font=("Arial", 14, "bold"),
            anchor="center",
        )
        self.filter_with_label = ctk.CTkLabel(self.filter_change_container, text=self._get_text("Filter With"),
            fg_color=GUI_DC.DARK_BACKGROUND,
            bg_color=GUI_DC.DARK_BACKGROUND,
            text_color=GUI_DC.LIGHT_TEXT_COLOR,
            font=("Arial", 14, "bold"),
            anchor="center",
        )
        self.operation_label = ctk.CTkLabel(self.filter_change_container, text=self._get_text("Operation"),
            fg_color=GUI_DC.DARK_BACKGROUND,
            bg_color=GUI_DC.DARK_BACKGROUND,
            text_color=GUI_DC.LIGHT_TEXT_COLOR,
            font=("Arial", 14, "bold"),
            anchor="center",
        )

        # Check when no filter is selected. Just show the filter by label.
        if self.current_filtering == [] :
            self.filter_by_label.grid(row=0, column=0, columnspan=3, padx=GUI_DC.INNER_PADDING)
        else :
            # Check if filter exists. Than, show all info labels.
            self.filter_by_label.grid(row=0, column=0, padx=GUI_DC.INNER_PADDING)
            self.filter_with_label.grid(row=0, column=1, padx=GUI_DC.INNER_PADDING)
            self.operation_label.grid(row=0, column=2, padx=GUI_DC.INNER_PADDING)

        # Iterate over the current filterings.
        for grid_row_index, current_filter in enumerate(self.current_filtering) :

            # Increase the grid row index. The initial must be allocated for the info labels.
            grid_row_index += 1

            # Get the current filter key and value.
            current_filter_key = self.available_filterings_show_display[current_filter["filter_key"]]
            current_filter_value = current_filter["filter_value"]
            
            def ___WRAPS_remove_filter(filter : dict = current_filter) -> None:
                """
                A warpper function for combobox handlings. The reason its seperated is to avoid the closure problem.
                @Parameters:
                    filter - Required : The filter to remove. (dict) -> Which is the filter to remove from the current filterings.
                @Returns:
                    None
                """
                # Call the remove filter function.
                self.__remove_filter(filter)

            # Create the widgets.
            current_filter_key_label = ctk.CTkLabel(self.filter_change_container, text=current_filter_key,
                fg_color=GUI_DC.DARK_BACKGROUND,
                bg_color=GUI_DC.DARK_BACKGROUND,
                text_color=GUI_DC.LIGHT_TEXT_COLOR,
                font=("Arial", 13, "bold"),
                anchor="center",
            )
            current_filter_key_label.grid(row=grid_row_index, column=0)

            current_filter_value_label = ctk.CTkLabel(self.filter_change_container, text=current_filter_value,
                fg_color=GUI_DC.DARK_BACKGROUND,
                bg_color=GUI_DC.DARK_BACKGROUND,
                text_color=GUI_DC.LIGHT_TEXT_COLOR,
                font=("Arial", 13, "bold"),
                anchor="center",
            )
            current_filter_value_label.grid(row=grid_row_index, column=1)

            remove_filter_button = ctk.CTkButton(self.filter_change_container, text=self._get_text("Remove"), command=___WRAPS_remove_filter,
                fg_color=GUI_DC.LIGHT_BACKGROUND,
                bg_color=GUI_DC.DARK_BACKGROUND,
                hover_color=GUI_DC.SECONDARY_LIGHT_BACKGROUND,
                text_color=GUI_DC.DARK_TEXT_COLOR,
                text_color_disabled=GUI_DC.MEDIUM_TEXT_COLOR,
                anchor="center",
                font=("Arial", 12, "bold")
            )
            remove_filter_button.grid(row=grid_row_index, column=2, padx=GUI_DC.INNER_PADDING, pady=GUI_DC.INNER_PADDING)

        # Create the filter key combobox.
        self.binder_variable = ctk.StringVar()
        self.filter_key_combobox = ctk.CTkComboBox(self.filter_change_container, values=list(self.available_filterings_text_display.keys()), variable=self.binder_variable,
            justify="center",
            state="readonly",
        )
        self.filter_key_combobox.grid(row=self.row_count-1, column=0, padx=GUI_DC.INNER_PADDING, pady=GUI_DC.INNER_PADDING)

        # Bind the combobox to move to the next step. When key selected.
        self.binder_variable.trace_add("write", self.__load_filter_value_combobox)

    def __load_filter_value_combobox(self, *args, **kwargs) -> None:
        """
        Loads the filter value combobox with the values of the selected filter key.
        @Parameters:
            event - Required : The event that triggered the function. (tk.Event) -> The event that triggered the function.
        @Returns:
            None
        """
        # Remove old label and re-init widgets.
        self.filter_by_label.grid_forget()

        # Init the operation info labels.
        self.filter_by_label.grid(row=0, column=0, padx=GUI_DC.INNER_PADDING)
        self.filter_with_label.grid(row=0, column=1, padx=GUI_DC.INNER_PADDING)
        self.operation_label.grid(row=0, column=2, padx=GUI_DC.INNER_PADDING)

        # Try to get values
        try :
            values = self.available_filterings[self.available_filterings_text_display[self.filter_key_combobox.get()]]
        except KeyError :
            values = []

        # Set the new filter value combobox.
        self.filter_value_combobox = ctk.CTkComboBox(self.filter_change_container, values=values,
            justify="center",
            state="readonly",
        )
        self.filter_value_combobox.grid(row=self.row_count-1, column=1, padx=GUI_DC.INNER_PADDING, pady=GUI_DC.INNER_PADDING)

        # Set the new add filter button.
        self.add_filter_button = ctk.CTkButton(self.filter_change_container, text=self._get_text("Add"), command=self.__add_filter,
            fg_color=GUI_DC.LIGHT_BACKGROUND,
            bg_color=GUI_DC.DARK_BACKGROUND,
            hover_color=GUI_DC.SECONDARY_LIGHT_BACKGROUND,
            text_color=GUI_DC.DARK_TEXT_COLOR,
            text_color_disabled=GUI_DC.MEDIUM_TEXT_COLOR,
            anchor="center",
            font=("Arial", 12, "bold")
        )
        self.add_filter_button.grid(row=self.row_count-1, column=2, padx=GUI_DC.INNER_PADDING, pady=GUI_DC.INNER_PADDING)

    def __add_filter(self) -> None:
        """
        Adds a new filter to the current_filtering list
        @Parameters:
            None
        @Returns:
            None
        """
        # Get filter value and key
        taken_filter_key = self.available_filterings_text_display[self.filter_key_combobox.get()]
        taken_filter_value = self.filter_value_combobox.get()

        # Check if the new filter exists
        for current_filter in self.current_filtering :
            if current_filter["filter_key"] == taken_filter_key and current_filter["filter_value"] == taken_filter_value :
                messagebox.showerror(self._get_text("Error"), self._get_text("This filter already exists"))
                return
            
        # Check if the new filter_key or filter_value is empty
        if taken_filter_value == "" :
            messagebox.showerror(self._get_text("Error"), self._get_text("Please select a filter value"))
            return

        # Add the new filter to the current_filtering list
        self.current_filtering.append({"filter_key" : taken_filter_key, "filter_value" : taken_filter_value})

        # Clear and re-init the filter_change_container.
        self.filter_key_combobox.destroy()
        self.filter_value_combobox.destroy()
        self.add_filter_button.destroy()

        # Init all filters back on display.
        self._init_filters()

    def __remove_filter(self, current_filter : dict) -> None:
        """
        Remove a filter from the current filterings.
        @Parameters:
            current_filter - Required : The filter to remove. (dict) -> {filter_key : str, filter_value : str}
        @Returns:
            None
        """
        # Directly remove from literal.
        self.current_filtering.remove(current_filter)

        # Clear and re-init the filter_change_container.
        self.filter_change_container.destroy()
        self.filter_change_container = ctk.CTkFrame(self.widgets_container, fg_color=GUI_DC.DARK_BACKGROUND, bg_color=GUI_DC.DARK_BACKGROUND)
        self.filter_change_container.grid(row=1, column=0, columnspan=2, padx=GUI_DC.INNER_PADDING, pady=GUI_DC.INNER_PADDING)
        
        # Init all filters back on display.
        self._init_filters()

    def get_result(self) -> list:
        """
        Get the result of the dialog.
        @Parameters:
            None
        @Returns:
            result (dict) : The result of new filterings.
        """
        # Return the result.
        return self.result

    def __save(self) -> None:
        """
        Save the changes and exit the dialog.
        @Parameters:
            None
        @Returns:
            None
        """
        # check if the new filter_value is empty.
        try :
            if self.filter_value_combobox.get() == "" :
                messagebox.showerror(self._get_text("Error"), self._get_text("Please select a filter value"))
                return
        except :
            pass

        # Set the result to the current filtering.
        self.result = self.current_filtering

        # Destroy the dialog.
        self.destroy()

    def __clean_exit(self) -> None:
        """
        Clean exit from the dialog.
        @Parameters:
            None
        @Returns:
            None
        """
        # Set the result to None. (It is None by default.).
        self.result = self.result
        # Destroy the dialog.
        self.destroy()
