# OPENCV APPLICATION EXAMPLES

This Repo contains a collection of OpenCV project codes that I implemented for research and study purpose. I am currently working on re-organizing this repo as well as adding new opencv application code every week. Most applications were written in Python, however, I am going to add C++ version for all of them very soon.

## Application Menu

| Application  | Description           | Demo        |
|---------------|--------------------------|-------------|
| Chroma Key Green Screen <br/> Background Removal | Remove chroma key green background from images & videos. This is a popular technique in video making. My implementation makes use of YCrCb Color Space & the calculation of color distance.<br/> Techniques: **YCrCb Color Space, Color Distance** | <img height="200px" src="/Chroma_Keying/output/testing.gif" alt="chroma"> |
| Document Scanner | A simple document scanner for photo images, with some additional features to enhance the quality of the output image.<br />Techniques: **Perspective Transformation, Contour Approximation, Adaptive Thresholding**  | <img height="250px" src="/Document_Scanner/demo.gif" alt="scanner"> |
| Blemish Remover  | Remove blemishes on a person face, making the facial skin region looks smooth & consistent.<br />Techniques: **Seamless Cloning, Image Gradients** | <img height="150px" src="/Blemish_Remover/blemish.png" alt="raw"> <img height="150px" src="/Blemish_Remover/edited.png" alt="processed"> |
| Smile Detection | Detect smiling faces. Using only Dlib for facial landmark approximation. Smiles are detected by checking lips width vs jaw width ratio. A Deep Learning approach will be added soon.<br />Techniques: **Facial Landmark Detection, Haar Cascade** | <img height="150px" src="/Smile_Detection/smile_output.jpg" alt="smile"> |
| Face Morphing | Perform face morphing from one person's face to another.<br />Techniques: **Facial Landmark Detection, Delaunay Triangulation, Alpha Blending** | <img height="150px" src="/Face_Morphing/output.gif" alt="face_mprph"> |
| Facial Makeup | Automatically apply some makeup on a person face. There are currently 2 features: applying lipstick color & applying color for eye lenses. More options will be added soon.<br />Techniques: **Facial Landmark Detection, Image Thresholding & Masking** | <img height="150px" src="/resources/images/girl-no-makeup.jpg" alt="girl_raw"> <img height="150px" src="/Facial_Makeup/output.jpg" alt="girl_edited">  |

