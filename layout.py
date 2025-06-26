import gradio as gr

css = """
.image-locator {
    display: block;
    margin-left: auto;
    margin-right: auto;
    }
"""

theme = gr.themes.Base(
    primary_hue="rose",
    neutral_hue="cyan",
).set(
    body_background_fill='*neutral_200',
    background_fill_primary='*neutral_100',
    input_background_fill='*neutral_50',
    checkbox_background_color_hover='*neutral_200',
    checkbox_label_background_fill='*neutral_200',
    button_secondary_text_color='*neutral_800',
 
    section_header_text_size='*text_lg',

    container_radius='*radius_xl', # The corner radius of a layout component that holds other content.
    block_radius='*radius_xl', # The corner radius around an item.
    checkbox_border_radius='*radius_lg',
    input_radius='*radius_xl',

    block_border_width='0px',
 

)