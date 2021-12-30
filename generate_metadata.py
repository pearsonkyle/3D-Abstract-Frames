import os
import glob
import json

from ipfs import sample_metadata

if __name__ == "__main__":

    model_dir = "/Users/kpearson/Programs/misc/SmartContract/3d_af/models/second_mint"
    out_dir = model_dir+"_metadata"
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)

    models = glob.glob(os.path.join(model_dir,"*.glb"))

    # folder of uploaded data
    base_url = "https://gateway.pinata.cloud/ipfs/QmVaVUhzLyoq2AXEHziAFni5a4xWY2Tuei9sGxPa8256Yc/"

    for m, model in enumerate(models):
    
        # check for image
        if not os.path.exists(model.replace(".glb", "_render.png")):
            continue

        model_link = os.path.join(base_url,os.path.basename(model))
        image_link = os.path.join(base_url,os.path.basename(model.replace(".glb", "_render.png")))

        newmeta = dict(sample_metadata)
        newmeta['name'] = f"3D Abstract Frame #{m+1+24}"
        newmeta['description'] = f"Generative 3d collectibles minted on the Polygon blockchain.\n\nHolders of this token will continue to be rewarded with new metaverse integrations forever.\nView this model in Augmented Reality (AR) using the [Galeri](https://www.galeri.co/) app.\n\nDownloads:\n\n [Full Image Render]({image_link})\n\n[3D .GLB File]({model_link})"
        newmeta['attributes'] = []

        hue, twirl, rot, noise, _,_,_ = os.path.basename(model).split('_')
        newmeta['attributes'].append({"trait_type": "Hue", "value": str(round(float(hue),2))})
        newmeta['attributes'].append({"trait_type": "Twirl", "value": str(round(float(twirl),2))})
        newmeta['attributes'].append({"trait_type": "Rotation", "value": str(round(float(rot),2))})
        newmeta['attributes'].append({"trait_type": "Noise", "value": str(round(float(noise),2))})
        newmeta['external_url'] = "https://www.galeri.co/"

        # publish metadata to ipfs
        newmeta['image'] = image_link
        newmeta['animation_url'] = os.path.join(base_url,os.path.basename(model))
        print(json.dumps(newmeta,indent=4))

        jname = os.path.join(out_dir,os.path.basename(model.replace("glb","json")))
        with open(jname, 'w') as outfile:
            json.dump(newmeta, outfile, indent=4)