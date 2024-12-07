import streamlit as st
import sys
sys.path.insert(0, "../Sidebar")
from streamlit_folium import folium_static 


def footer_info():
# Connect file to style.css
    with open("./css/style.css") as f:
        st.markdown(
            f"""<style>{f.read()}</style>""",
            unsafe_allow_html=True,
        )
        

    # Create sections for anchor tags and background info
    col1, col2 = st.columns([0.4, 0.6])

    with col1:
        # Anchor tags
        st.markdown('''
            - [Introduction](#introduction)
            - [About the EPA Data and its Limitations](#about-the-epa-data-and-its-limitations)
            - [Links to Data](#links-to-data)
            - [About the Authors](#about-the-authors)
            - [About EDGI](#about-edgi)
        ''', unsafe_allow_html=True)

    sub_heading_style = """
        color: #B3611E;
        font-family: Inter;
        font-size: 28px;
        font-style: normal;
        font-weight: 600;
        line-height: 150%;
        letter-spacing: -0.644px;
    """

    description_style = """
        color: var(--black, #101010);
        font-family: Open Sans;
        font-size: 22px;
        font-style: normal;
        font-weight: 600;
        line-height: 150%; /* 33px */
        letter-spacing: -0.506px;
    """

    with col2:
        st.header('Introduction')
        st.markdown(f"""
            <div class="intro">
            <h2 class="sub-heading" style="{sub_heading_style}">
                Why Report Cards on compliance with and enforcement of Environmental Laws?
            </h2>
            <p class="description" style="{description_style}">
                The Environmental Protection Agency (EPA) is charged by Congress to enforce laws that protect people from air pollution, water pollution and hazardous waste. Without effective enforcement, these laws are meaningless. Based on data from EPA’s Enforcement and Compliance History Online (ECHO) database this report card reviews violations, inspections and enforcement actions under three laws: Clean Air Act (CAA), Clean Water Act (CWA) and Resource Conservation and Recovery Act (RCRA) for this Congressional District or State since 2001. Report cards like this one are becoming available on the EEW website for all House Representatives and Senators. The EEW website also has a summary analysis of enforcement trends and data issues for all geographies covered by the House Energy and Commerce and Senate Environment and Public Works Committees. The report cards contain data from both state environmental agencies and the EPA. If the states are enforcing the above laws, it is because the EPA has delegated that authority to them. The EPA must ensure that states are doing their job. Congress must ensure that the EPA is doing its job. And the public must have accurate data from states and the EPA in order to understand if national environmental laws are being properly enforced. For the first time, EEW Congressional Report Cards give members of Congress and their constituents the chance to evaluate whether the EPA is fulfilling its mandate in their district. Congress can strengthen EPA enforcement by increasing its budget, passing more effective laws, requiring better data collection, and holding the EPA accountable when it fails to protect people.
            </p>
            <h2 class="sub-heading" style="{sub_heading_style}">
                What is a regulated facility?
            </h2>
            <p class="description" style="{description_style}">
                A regulated facility in this report is a facility that reports air or water emissions under the Clean Air Act or Clean Water Act, or a facility that generates, transports, or disposes of hazardous waste under the Resource Conservation and Recovery Act. Regulated facilities can be large-scale e.g. oil refineries, or small-scale e.g. dry cleaners.
            </p>
            </div>
        """, unsafe_allow_html=True)


        st.image('./images/regulated_facility.png', use_column_width=True)
        st.header('About the EPA Data and its Limitations')
        st.markdown(f"""
            <div class="about_epa_data">
            <p class="description">
                The data in this report is from EPA’s publicly-available ECHO database that compiles information from a number of distinct state and federal sources. However, poor reporting by states and inconsistent reporting schemes result in data gaps and inaccuracies. EPA lists numerous specific issues on its “Known Data Problems” page. In addition, EPA notes that data on inspections, violations, and enforcement actions prior to 2001 should be treated as incomplete and unreliable. For that reason, we have only tracked data back to 2001. In addition to many data entry errors – too numerous to list here – there are several major problems with ECHO:
            </p>
            <ul class="description-list">
                <li class="list-text">
                There is serious under-recording and under-reporting of CAA violations at the state level. Most CAA violations – perhaps 85% or more – do not make it into ECHO. Violation data is therefore inaccurate and misleading: <span class="bold-text">states which report the fewest violations may be states whose recording and reporting of violations is actually the poorest.</span>
                </li>
                <li class="list-text">
                Although there is no specific information about the quality of data on RCRA violations, it is likely that this program, like the CAA, has serious reporting problems. Therefore, RCRA violations data should also be considered inaccurate and potentially misleading. The key difference between these and the CWA is that the CWA entails mandatory electronic self-reporting.
                </li>
                <li class="list-text">
                ECHO does not record how many regulated facilities there were for programs in previous years. Therefore, we cannot calculate the number of inspections, enforcement actions, and violations per regulated facility before 2022.
                </li>
            </ul>
            <h2 class="sub-heading">
                Data reliability coding
            </h2>
            <p class="description">
                In this report, we have divided data issues into three categories, using transparencies in graphs as well as subtitles to indicate data reliability and completeness. See the table below:
            </p>
            </div>
        """, unsafe_allow_html=True)
        st.image('./images/data_reliability_coding.png', use_column_width=True)
        st.markdown(f"""
            <div class="about_epa_data">
            <h2 class="sub-heading">
                Notes on 2023 data
            </h2>
            <p class="description">
                We do not include data from 2023 because it is be strongly influenced by the EPA’s decision to suspend, from March through August, pollution monitoring requirements for industries that claim to have been impacted by COVID-19. EDGI’s report on this policy “More Permission to Pollute” found that, despite relatively few facilities claiming the COVID exemption, a much larger proportion of facilities are still failing to report environmental data.
            </p>
            </div>
        """, unsafe_allow_html=True)
        st.header('Links to Data')
        st.markdown(f"""
            <div class="links_to_data">
            <h2 class="sub-heading">
                Useful Links
            </h2>
            <p class="description">
                This EEW project aims to make EPA data more directly accessible to the public and their representatives. With the goal of reaching the Representatives and Senators who oversee the EPA, EEW has made report cards for the 76 Senators and House Representatives that sit on the House Energy & Commerce Committee and the Senate Environment & Public Works Committee, as these committees are responsible for EPA oversight. By providing a novel look at the chronic state of non-compliance in their states and districts, we hope to provide these key representatives with the information they need to evaluate the state of environmental law compliance and enforcement in their communities so they might more effectively hold EPA accountable
            </p>
            </div>
        """, unsafe_allow_html=True)
        st.header('About the Authors')
        st.markdown(f"""
            <div class="about_the_authors">
            <h2 class="sub-heading">
                About EEW
            </h2>
            <p class="description">
                Environmental Enforcement Watch (EEW) is a collaborative project across working groups of the Environmental Data and Governance Initiative (EDGI). The EEW project builds on EDGI’s 2019 Sheep in the Closet Report that documents large declines in EPA enforcement of environmental laws. This project uses data from EPA’s ECHO database, revealing how useful ECHO could be for communities to track pollution and EPA responses in their areas. However, it also reveals the inaccessibility of ECHO for non-specialists, and major omissions, errors, and confusions present in the data itself (see page 10). EEW aims to highlight gaps and inadequacies in the enforcement of environmental laws and to help investigate whether EPA is fulfilling its congressionally-mandated duty to enforce environmental laws. EEW’s data analysis is conducted using open source and publicly available data using Jupyter Notebooks developed by EDGI members
            </p>
            <h2 class="sub-heading">
                About this Project
            </h2>
            <p class="description">
                This EEW project aims to make EPA data more directly accessible to the public and their representatives. With the goal of reaching the Representatives and Senators who oversee the EPA, EEW has made report cards for the 76 Senators and House Representatives that sit on the House Energy & Commerce Committee and the Senate Environment & Public Works Committee, as these committees are responsible for EPA oversight. By providing a novel look at the chronic state of non-compliance in their states and districts, we hope to provide these key representatives with the information they need to evaluate the state of environmental law compliance and enforcement in their communities so they might more effectively hold EPA accountable
            </p>
            </div>
        """, unsafe_allow_html=True)
        st.header('About EDGI')
        st.markdown(f"""
            <div class="about_edgi">
            <p class="description">
                EDGI is an international network of over 175 members from more than 80 different academic institutions and nonprofits, comprised foremost by grassroots volunteer efforts. Since 2016, EDGI has served as a preeminent watchdog group for federal environmental data, generating international effort to duplicate and monitor repositories of public data that are vital to environmental health research and knowledge. EDGI’s work has been widely acknowledged, leading to EDGI testifying before Congress on declines in EPA enforcement, and hundreds of mentions in leading national and international media such as The New York Times,The Washington Post, Vice News, and CNN. For more about our work, read our 2019 Annual Report and 2020 Annual Report. For more on EDGI see our website.
            </p>
            </div>
        """, unsafe_allow_html=True

        )




