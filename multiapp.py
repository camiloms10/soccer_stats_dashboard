"""Frameworks for running multiple Streamlit applications as a single app.
"""
import streamlit as st
from streamlit_option_menu import option_menu

class MultiApp:
    """Framework for combining multiple streamlit applications.
    Usage:
        def foo():
            st.title("Hello Foo")
        def bar():
            st.title("Hello Bar")
        app = MultiApp()
        app.add_app("Foo", foo)
        app.add_app("Bar", bar)
        app.run()
    It is also possible keep each application in a separate file.
        import foo
        import bar
        app = MultiApp()
        app.add_app("Foo", foo.app)
        app.add_app("Bar", bar.app)
        app.run()
    """
    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        """Adds a new application.
        Parameters
        ----------
        func:
            the python function to render this app.
        title:
            title of the app. Appears in the dropdown in the sidebar.
        """
        self.apps.append({
            "title": title,
            "function": func
        })

    def run(self):
        
        selected = option_menu(None, ["Home", "Dashboard", "Data"], 
        icons=['house', 'bar-chart-fill', "table"], 
        menu_icon="cast", default_index=0, orientation="horizontal",
            styles={
            #        "container": {"padding": "0!important", "background-color": "#52575c"},
            #        "icon": {"color": "white", "font-size": "20px"}, 
                    "nav-link": {
                                     #"font-size": "20px",
                                     #"text-align": "left",
                                     "margin":"0px",
                                     "--hover-color": "#bebebe"},
            #        "nav-link-selected": {"background-color": "black"},
            }
            )

        if selected == "Home":
            app = self.apps[0]
        if selected == "Dashboard":
            app = self.apps[1]    
        if selected == "Data":
            app = self.apps[2]

        app['function']()