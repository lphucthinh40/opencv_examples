# OPENCV APPLICATION EXAMPLES

This Repo contains a collection of OpenCV project codes that I implemented for research and study purpose. I am currently working on re-organizing this repo as well as adding new opencv application code every week. Most applications were written in Python, however, I am going to add C++ version for all of them very soon.

## Application Menu

| Application  | Description           | Demo        |
|---------------|--------------------------|-------------|
| Chroma Key Green Screen <br/> Background Removal | Remove chroma key green background from images & videos. This is a popular technique in video making. My implementation makes use of YCrCb Color Space & the calculation of color distance.<br/> Techniques: **YCrCb Color Space, Color Distance** | ![OpenCV](/Chroma_Keying/outut/testing.gif) |
| Document Scanner | A simple document scanner for photo images, with some additional features to enhance the quality of the output image.<br />Techniques: **Perspective Transformation, Contour Approximation, Adaptive Thresholding**  | ![enter image description here](https://upload.wikimedia.org/wikipedia/commons/thumb/3/32/OpenCV_Logo_with_text_svg_version.svg/1200px-OpenCV_Logo_with_text_svg_version.svg.png =250x250) |
| Blemish Remover  | Remove blemishes on a person face, making the facial skin region looks smooth & consistent.<br />Techniques: **Seamless Cloning, Image Gradients** | ![enter image description here](https://upload.wikimedia.org/wikipedia/commons/thumb/3/32/OpenCV_Logo_with_text_svg_version.svg/1200px-OpenCV_Logo_with_text_svg_version.svg.png =250x250) |
| Smile Detection | Detect smiling faces. Using only Dlib for facial landmark approximation. Smiles are detected by checking lips width vs jaw width ratio. A Deep Learning approach will be added soon.<br />Techniques: **Facial Landmark Detection, Haar Cascade** | ![enter image description here](https://upload.wikimedia.org/wikipedia/commons/thumb/3/32/OpenCV_Logo_with_text_svg_version.svg/1200px-OpenCV_Logo_with_text_svg_version.svg.png =250x250) |
| Face Morphing | Perform face morphing from one person's face to another.<br />Techniques: **Facial Landmark Detection, Delaunay Triangulation, Alpha Blending** | ![enter image description here](https://upload.wikimedia.org/wikipedia/commons/thumb/3/32/OpenCV_Logo_with_text_svg_version.svg/1200px-OpenCV_Logo_with_text_svg_version.svg.png =250x250) |
| Facial Makeup | Automatically apply some makeup on a person face. There are currently 2 features: applying lipstick color & applying color for eye lenses. More options will be added soon.<br />Techniques: **Facial Landmark Detection, Image Thresholding & Masking** | ![enter image description here](https://upload.wikimedia.org/wikipedia/commons/thumb/3/32/OpenCV_Logo_with_text_svg_version.svg/1200px-OpenCV_Logo_with_text_svg_version.svg.png =250x250) |

