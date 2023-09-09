from st_aggrid import AgGrid
import streamlit as st
import pandas as pd
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode, JsCode
df = pd.read_csv('https://raw.githubusercontent.com/fivethirtyeight/data/master/airline-safety/airline-safety.csv')

# st.dataframe(df)

st.header("Customize AgGrid")
_function=st.sidebar.radio("Functions", ['Display', 'Highlight', 'Delete'])

gd = GridOptionsBuilder.from_dataframe(df)
gd.configure_pagination(paginationAutoPageSize=True, paginationPageSize=10)
gd.configure_side_bar()
gd.configure_grid_options(domLayout='normal',rowHeight=50)
gd.configure_default_column(groupable=True, value=True, enableRowGroup=True, editable=True)
gd.configure_selection('multiple', use_checkbox=True)

sel_mode = st.selectbox("Selection Mode", ['single', 'multiple'])
gd.configure_selection(sel_mode, use_checkbox=True, groupSelectsChildren=True, groupSelectsFiltered=True)
grid_table = AgGrid(df, gridOptions=gd.build(), 
                    height=500, 
                    width='100%', 
                    data_return_mode=DataReturnMode.AS_INPUT, 
                    update_mode=GridUpdateMode.MODEL_CHANGED)
selected_rows = grid_table['selected_rows']
st.write(selected_rows)

if _function == 'Highlight':
    if st.sidebar.button("Highlight"):
        grid_table.api.apply_to_selected_rows(JsCode("""function(params) {
            params.node.setRowHeight(100);
            params.node.setDataValue('airline', 'highlighted');
        }"""))
    
if _function == 'Delete':
    if st.sidebar.button("Delete"):
        grid_table.api.delete_selected_rows()
    
    