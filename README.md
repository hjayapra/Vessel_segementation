# Vessel_segementation
SAM Segment-anything-model adaptation for T2 Vessel segmentation
Imported Brain Vein T2 images from Geriatric Psychiatry Neuroimaging lab and set the path 
convert_gz_to_nii Function converts .nii.gz files to .nii files
Install all necessary packages including SimpleITK 
Use MIPs (Maximum Intensity Projection) to visualize the vessels in each image 
Normalize the data and map the MIP images to 3D 
Apply adaptive thresholding to the MIP images 

Use the SAMAutomaticMaskGenerator Class 
Set the chekpoint to the SAM model 
Adjust tunable parameters as needed 
