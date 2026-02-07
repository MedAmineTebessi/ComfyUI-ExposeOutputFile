import os
class ExposeOutputFile:
    """
    Takes a path string (like '3D/Hy3D_00001.glb' or '/opt/ComfyUI/output/3D/Hy3D_00001.glb')
    and exposes it as a ComfyUI UI output so comfyui-api can return/upload it.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "path": ("STRING", {"default": "", "multiline": False})
            },
            "optional": {
                "webhook_url": ("STRING", {"default": "", "multiline": False}),
                "job_id": ("STRING", {"default": "", "multiline": False})
            }
        }

    RETURN_TYPES = ()
    FUNCTION = "expose"
    CATEGORY = "utils"
    OUTPUT_NODE = True

    def expose(self, path: str, webhook_url: str = "", job_id: str = ""):
        p = (path or "").replace("\\", "/").strip()

        # Upload to Webhook if provided (Bypass S3 issues)
        if webhook_url and webhook_url.startswith("http"):
            try:
                print(f"Uploading {p} to {webhook_url}...")
                import requests
                
                # Check if file exists
                if os.path.exists(path):
                    with open(path, 'rb') as f:
                        response = requests.post(
                            webhook_url, 
                            files={'file': f},
                            data={'jobId': job_id}
                        )
                    print(f"Webhook response: {response.status_code} - {response.text}")
                else:
                    print(f"File not found for webhook: {path}")
            except Exception as e:
                print(f"Webhook upload failed: {e}")
                import traceback
                traceback.print_exc()

        # Make it robust to different path styles
        # Strip anything up to and including output/ or outputs/
        for marker in ["/output/", "output/", "/outputs/", "outputs/"]:
            if marker in p:
                p = p.split(marker, 1)[1]

        p = p.lstrip("/")  # now should be relative like "3D/Hy3D_00001.glb"
        filename = os.path.basename(p)
        subfolder = os.path.dirname(p)

        results = [{
            "filename": filename,
            "subfolder": subfolder,
            "type": "output"
        }]

        return {"ui": {"images": results}}

NODE_CLASS_MAPPINGS = {
    "ExposeOutputFile": ExposeOutputFile
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ExposeOutputFile": "Expose Output File (for API)"
}