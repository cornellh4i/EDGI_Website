import streamlit as st
import sys
sys.path.insert(0, "../Sidebar")
from streamlit_folium import folium_static 


def footer_info():
# Connect file to style.css
    with open("../css/style.css") as f:
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

        st.header('About the EPA Data and its Limitations')
        st.write('''
        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Amet volutpat consequat mauris nunc congue nisi vitae suscipit tellus. Amet mauris commodo quis imperdiet. In metus vulputate eu scelerisque. Facilisis gravida neque convallis a cras semper. Quis vel eros donec ac odio. Posuere urna nec tincidunt praesent semper feugiat nibh sed. Vitae et leo duis ut. Consectetur lorem donec massa sapien faucibus et molestie ac feugiat. Scelerisque varius morbi enim nunc faucibus a. Eget velit aliquet sagittis id consectetur purus ut. Massa eget egestas purus viverra. Libero justo laoreet sit amet cursus sit. Nibh nisl condimentum id venenatis a condimentum vitae sapien.
        ''')

        st.header('Links to Data')
        st.write('''
        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Amet volutpat consequat mauris nunc congue nisi vitae suscipit tellus. Amet mauris commodo quis imperdiet. In metus vulputate eu scelerisque. Facilisis gravida neque convallis a cras semper. Quis vel eros donec ac odio. Posuere urna nec tincidunt praesent semper feugiat nibh sed. Vitae et leo duis ut. Consectetur lorem donec massa sapien faucibus et molestie ac feugiat. Scelerisque varius morbi enim nunc faucibus a. Eget velit aliquet sagittis id consectetur purus ut. Massa eget egestas purus viverra. Libero justo laoreet sit amet cursus sit. Nibh nisl condimentum id venenatis a condimentum vitae sapien.
        ''')

        st.header('About the Authors')
        st.write('''
        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Amet volutpat consequat mauris nunc congue nisi vitae suscipit tellus. Amet mauris commodo quis imperdiet. In metus vulputate eu scelerisque. Facilisis gravida neque convallis a cras semper. Quis vel eros donec ac odio. Posuere urna nec tincidunt praesent semper feugiat nibh sed. Vitae et leo duis ut. Consectetur lorem donec massa sapien faucibus et molestie ac feugiat. Scelerisque varius morbi enim nunc faucibus a. Eget velit aliquet sagittis id consectetur purus ut. Massa eget egestas purus viverra. Libero justo laoreet sit amet cursus sit. Nibh nisl condimentum id venenatis a condimentum vitae sapien.
        ''')

        st.header('About EDGI')
        st.write('''
        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Amet volutpat consequat mauris nunc congue nisi vitae suscipit tellus. Amet mauris commodo quis imperdiet. In metus vulputate eu scelerisque. Facilisis gravida neque convallis a cras semper. Quis vel eros donec ac odio. Posuere urna nec tincidunt praesent semper feugiat nibh sed. Vitae et leo duis ut. Consectetur lorem donec massa sapien faucibus et molestie ac feugiat. Scelerisque varius morbi enim nunc faucibus a. Eget velit aliquet sagittis id consectetur purus ut. Massa eget egestas purus viverra. Libero justo laoreet sit amet cursus sit. Nibh nisl condimentum id venenatis a condimentum vitae sapien.
        ''')
