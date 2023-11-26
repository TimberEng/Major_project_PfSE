import streamlit as st
import plotly.graph_objects as go
import app_module as appmo
from plotly import graph_objects as go
import plotly.express as px
from Structural_Analysis import analysis

st.markdown('# Structural Analysis Project')
st.markdown('## Project details as below:') 
st.markdown('A gabled-roof portal frame, shown below, is constructed from a grade 300MPa structural steel cross-section, which could be selected from the left dropdown menu. The portal frame is mainly to resist uniformly distributed wind pressure (WP, not shown in Fig). Given the specified height (H) and roof angle (α), what would be the longest span length (L) for this frame to satisfy all the flexural, shear, and deflection design criteria?')



st.sidebar.subheader("Parameter Inputs")

SectionName = st.sidebar.selectbox(
   "UB Section",
    appmo.col
)



Column_height = st.sidebar.number_input("Column height (mm)", value=3500, step= 100)
pressure = st.sidebar.number_input("Uniformly distributed wind pressure, Wp (kPa)", value=3.0, step= 1.0)
Angle = st.sidebar.number_input("Roof angle (deg)", value=10.0, step= 1.0)
Length = st.sidebar.number_input("Span length (mm)", value=10000.0, step= 100.0)

Iy = appmo.section_df.loc[SectionName]['Iy']
Iz = appmo.section_df.loc[SectionName]['Iz']
It = appmo.section_df.loc[SectionName]['It']
A = appmo.section_df.loc[SectionName]['A']
h = appmo.section_df.loc[SectionName]['h']
dw = appmo.section_df.loc[SectionName]['hi']
tw = appmo.section_df.loc[SectionName]['tw']

frame_model = appmo.build_frame(Column_height, Length, pressure, Angle, Iy, Iz, It, A)


edges = [
    [0, 1],
    [1, 2],
    [2, 3],
    [3, 4]
]

colors = ['rgb(255,0,0)', 'rgb(0,255,0)', 'rgb(0,0,255)', 'rgb(0,0,0)']

Frame_fig = go.Figure()
for index, (i_node, j_node) in enumerate(edges):
    x_coord_i = appmo.get_nodes(frame_model)[0][i_node]
    y_coord_i = appmo.get_nodes(frame_model)[1][i_node]
    x_coord_j = appmo.get_nodes(frame_model)[0][j_node]
    y_coord_j = appmo.get_nodes(frame_model)[1][j_node]
    trace = go.Scatter(
        x = [x_coord_i, x_coord_j],
        y = [y_coord_i, y_coord_j],
        line = {
            'color': colors[index],
            'width': 5
        },
        marker={
            'size': 10
        },
        showlegend = False
    )
    Frame_fig.add_trace(trace)

Frame_fig.layout.height=600
Frame_fig.layout.width=800
Frame_fig.layout.xaxis.title = "Span length (mm)"
Frame_fig.layout.yaxis.title = "Height (mm)"
Frame_fig


# Design criterion calculation
moment_cri = analysis.flexural_cri(300, Iy, h/2)
shear_cri = analysis.shear_cri(300, dw, tw)
v_cri = analysis.ver_defl(Length)
h_cri = analysis.laterl_dri(Column_height)

# Max values from FE model
max_moment = appmo.find_max_moment(frame_model)
max_shear= appmo.find_max_shear(frame_model)
max_vertical = appmo.find_max_vertical(frame_model)
max_horizontal= appmo.find_max_horizontal(frame_model)

# Engineering check

moment_check = analysis.eng_check("Moment",  max_moment,moment_cri)
shear_check = analysis.eng_check("Shear", max_shear, shear_cri)
h_check = analysis.eng_check("Horizontal displacement", max_horizontal, h_cri)
v_check = analysis.eng_check("Vertical displacement", max_vertical, v_cri)

    
tab2, tab3, tab4, tab5 = st.tabs(['Shear Desing', 'Bending Moment Desing','Vertical Displacment Desing','Horizontal Displacment Desing'])
with tab2: #SFD
    st.write(f"Max shear force based on seleted UB Section: {round(max_shear, 2)} kN")
    st.write(f"Shear desgin criterion: {shear_cri} kN")
    st.write(f"{shear_check}")
    Shear_fig = go.Figure()
    Shear_fig.add_trace(go.Scatter(x = appmo.get_list(frame_model)[0][0][0],
                                   y = appmo.get_list(frame_model)[0][0][1] /1000,
                                   name="Member 1",
                                   line=dict(color = colors[0], width = 4)))
    Shear_fig.add_trace(go.Scatter(x = appmo.get_list(frame_model)[0][1][0],
                                   y = appmo.get_list(frame_model)[0][1][1] /1000,
                                   name="Member 2",
                                   line=dict(color = colors[1], width = 4)))
    Shear_fig.add_trace(go.Scatter(x = appmo.get_list(frame_model)[0][2][0],
                                   y = appmo.get_list(frame_model)[0][2][1] /1000,
                                   name="Member 3",
                                   line=dict(color = colors[2], width = 4)))
    Shear_fig.add_trace(go.Scatter(x = appmo.get_list(frame_model)[0][3][0],
                                   y = appmo.get_list(frame_model)[0][3][1] /1000,
                                   name="Member 4",
                                   line=dict(color = colors[3], width = 4)))
    Shear_fig.layout.xaxis.title = "Member length (mm)"
    Shear_fig.layout.yaxis.title = "Member shear force (kN)"
    Shear_fig

with tab3: #BMD
    st.write(f"Max bending moment based on seleted UB Section: {round(max_moment,2)} kNm")
    st.write(f"Bending moment criterion: {round(moment_cri,2)} kNm")
    st.write(f"{moment_check}")
    Moment_fig = go.Figure()
    Moment_fig.add_trace(go.Scatter(x = appmo.get_list(frame_model)[1][0][0],
                                    y = appmo.get_list(frame_model)[1][0][1]/10**6,
                                    name="Member 1",
                                   line=dict(color = colors[0], width = 4)))
    Moment_fig.add_trace(go.Scatter(x = appmo.get_list(frame_model)[1][1][0],
                                    y = appmo.get_list(frame_model)[1][1][1]/10**6,
                                    name="Member 2",
                                   line=dict(color = colors[1], width = 4)))
    Moment_fig.add_trace(go.Scatter(x = appmo.get_list(frame_model)[1][2][0],
                                    y = appmo.get_list(frame_model)[1][2][1]/10**6,
                                    name="Member 3",
                                   line=dict(color = colors[2], width = 4)))
    Moment_fig.add_trace(go.Scatter(x = appmo.get_list(frame_model)[1][3][0],
                                    y = appmo.get_list(frame_model)[1][3][1]/10**6,
                                    name="Member 4",
                                   line=dict(color = colors[3], width = 4)))
    Moment_fig.layout.xaxis.title = "Member length (mm)"
    Moment_fig.layout.yaxis.title = "Member bending moment(kNm)"
    Moment_fig

with tab4: #V disp
    st.write(f"Max vertical displacement based on seleted UB Section: {round(max_vertical,2)} mm")
    st.write(f"Vertival criterion: {round(v_cri,2)} mm")
    st.write(f"{v_check}")
    Vertical_dis_fig = go.Figure()
    Vertical_dis_fig.add_trace(go.Scatter(x = appmo.get_list(frame_model)[2][0][0],
                                          y = appmo.get_list(frame_model)[2][0][1],
                                          name="Memnber 1",
                                   line=dict(color = colors[0], width = 4)))
    Vertical_dis_fig.add_trace(go.Scatter(x = appmo.get_list(frame_model)[2][1][0],
                                          y = appmo.get_list(frame_model)[2][1][1],
                                          name="Memnber 2",
                                   line=dict(color = colors[1], width = 4)))
    Vertical_dis_fig.add_trace(go.Scatter(x = appmo.get_list(frame_model)[2][2][0],
                                          y = appmo.get_list(frame_model)[2][2][1],
                                          name="Memnber 3",
                                   line=dict(color = colors[2], width = 4)))
    Vertical_dis_fig.add_trace(go.Scatter(x = appmo.get_list(frame_model)[2][3][0],
                                          y = appmo.get_list(frame_model)[2][3][1],
                                          name="Memnber 4",
                                   line=dict(color = colors[3], width = 4)))
    Vertical_dis_fig.layout.xaxis.title = "Member length (mm)"
    Vertical_dis_fig.layout.yaxis.title = "Member vertical displacement (mm)"
    Vertical_dis_fig

with tab5: #H disp
    st.write(f"Max horizontal displacement based on seleted UB Section: {round(max_horizontal,2)} mm")
    st.write(f"Horizontal criterion: {round(h_cri, 2)} mm")
    st.write(f"{h_check}")
    Horizontal_dis_fig = go.Figure()
    Horizontal_dis_fig.add_trace(go.Scatter(x = appmo.get_list(frame_model)[3][0][0],
                                            y = appmo.get_list(frame_model)[3][0][1],
                                            name="Member 1",
                                   line=dict(color = colors[0], width = 4)))
    Horizontal_dis_fig.add_trace(go.Scatter(x = appmo.get_list(frame_model)[3][1][0],
                                            y = appmo.get_list(frame_model)[3][1][1],
                                            name="Member 2",
                                   line=dict(color = colors[1], width = 4)))
    Horizontal_dis_fig.add_trace(go.Scatter(x = appmo.get_list(frame_model)[3][2][0],
                                            y = appmo.get_list(frame_model)[3][2][1],
                                            name="Member 3",
                                   line=dict(color = colors[2], width = 4)))
    Horizontal_dis_fig.add_trace(go.Scatter(x = appmo.get_list(frame_model)[3][3][0],
                                            y = appmo.get_list(frame_model)[3][3][1],
                                            name="Member 4",
                                   line=dict(color = colors[3], width = 4)))
    Horizontal_dis_fig.layout.xaxis.title = "Member length (mm)"
    Horizontal_dis_fig.layout.yaxis.title = "Member horizontal displacement (mm)"
    Horizontal_dis_fig