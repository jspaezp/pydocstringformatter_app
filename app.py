
import tempfile
import streamlit as st
import pydocstringformatter
from pydocstringformatter import __version__, _formatting, _utils
from pydocstringformatter._configuration.arguments_manager import ArgumentsManager
from pydocstringformatter._configuration.boolean_option_action import BooleanOptionalAction
import argparse

manager = ArgumentsManager(__version__, _formatting.FORMATTERS)

st.set_page_config(layout="wide")
st.header('PyDocstringFormatter')
st.write('Version: {}'.format(__version__))
st.write('This tool is a wrapper around the PyDocstringFormatter library. '
        'It provides a web interface to the library. ')


col1, col2 = st.columns(2)

def execute():
    query = []
    query.extend([x for x in bool_act_elems if x != ""])
    query.extend([y for x, y in zip(store_true_actions_elems, store_true_actions) if x])
    for x, y in zip(store_actions_elems, store_actions):
        if x != "":
            query.append(y)
            query.append(x)
    for action_name, selected_items in extend_actions_elems.items():
        for item in selected_items:
            query.append(action_name)
            query.append(item)

    with tempfile.TemporaryDirectory() as tmpdir:
        with open(f"{tmpdir}/input.py", "w") as f:
            f.write(input_text)

        try:
            pydocstringformatter.run_docstring_formatter([f"{tmpdir}/input.py", "-w"] + query)
        except SystemExit as e:
            pass

        with open(f"{tmpdir}/input.py", "r") as f:
            output_text = f.read()


    with col1:
        st.subheader("Non formatted Python code:")
        st.code(input_text)
        st.markdown("> " + " ".join(query) + "\n")

    with col2:
        st.subheader("Formatted Python code:")
        st.code(output_text)

with st.form(key='my_form'):
    st.header('Options')
    submit_button = st.form_submit_button(label='Submit', on_click=execute)
    fcol1, fcol2, fcol3 = st.columns([1,1,2])

    with fcol1:


        bool_acts = [v.option_strings for k, v in manager.parser._option_string_actions.items() if isinstance(v, BooleanOptionalAction)]
        bool_acts = { item[0]: item for item in bool_acts }
        # [['--strip-whitespaces', '--no-strip-whitespaces'], ...]
        bool_act_elems = [st.selectbox(f"Select {k}", bool_act, key=k) for k, bool_act in bool_acts.items()]


    with fcol2:

        store_actions_excluded = ["-w", "--quiet", "--exit-code"]
        store_true_actions = [v.option_strings for k, v in manager.parser._option_string_actions.items() if isinstance(v, argparse._StoreTrueAction)]
        store_true_actions = [x for x in store_true_actions if not any(y in store_actions_excluded for y in x)]
        store_true_actions = { item[0]: item for item in store_true_actions }
        # [..., ['--summary-quotes-same-line']]
        store_true_actions_elems = [st.checkbox(f"Select '{store_true_act[0]}'", value=False, key=store_true_act[0]) for k, store_true_act in store_true_actions.items()]
        store_actions_exclude = ["--exclude"]
        store_actions = [v.option_strings for k, v in manager.parser._option_string_actions.items() if isinstance(v, argparse._StoreAction)]
        store_actions = [x for x in store_actions if not any(y in store_actions_exclude for y in x)]
        store_actions = { x[0]: x for x in store_actions }
        # [['--max-summary-lines'], ['--max-line-length']]
        store_actions_elems = [st.text_input(f"Enter '{k}'", value="", key=k) for k, store_action in store_actions.items()]

        extend_actions = { v.option_strings[0]: v.choices for k, v in manager.parser._option_string_actions.items() if isinstance(v, argparse._ExtendAction) }
        extend_actions_elems = { k: st.multiselect(f"Select '{k}'", v) for k, v in extend_actions.items() }

    with fcol3:
        default_input = [
            'def foo(a, b):',
            '    """This is a docstring.',
            '    """',
            '    pass',]
        default_input = "\n".join(default_input)
        input_text = st.text_area("Python code", default_input, height=200)





# """
# for k, action in manager.parser._option_string_actions.items():
#     if isinstance(action, BooleanOptionalAction):
#         if value is True:
#             option = action.option_strings[0 if value is True else 1]
#             return [option]
# 
#     if isinstance(action, argparse._StoreTrueAction):
#         if value is True:
#             return [action.option_strings[0]]
#         return []
# 
#     if isinstance(action, argparse._StoreAction):
#         if isinstance(value, int):
#             value = str(value)
#         return [action.option_strings[0], value]
# 
#     if isinstance(action, argparse._ExtendAction):  # type: ignore[attr-defined]
#         out_args = []
#         if isinstance(value, list):
#             for item in value:
#                 out_args += [action.option_strings[0], item]
#         else:
#             out_args = [action.option_strings[0], value]
# 
#         return out_args
#     print(">>> ", k, ": ", v)
# 
# manager.parser._option_string_actions["--no-numpydoc-name-type-spacing"]
# 
# """