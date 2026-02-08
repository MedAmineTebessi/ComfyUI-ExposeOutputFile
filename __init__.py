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
        
        # Try to find the actual file by checking various locations
        possible_paths = [
            p,  # As provided
            os.path.join("/opt/ComfyUI/output", p),  # Standard ComfyUI output
            os.path.join("/opt/ComfyUI/output/3D", os.path.basename(p)),  # 3D subfolder
            os.path.join("/opt/ComfyUI/output", os.path.basename(p)),  # Just in output
            os.path.join("/comfyui/output", p),  # Alternative ComfyUI path
            os.path.join("/comfyui/output/3D", os.path.basename(p)),
        ]
        
        actual_file = None
        for check_path in possible_paths:
            if os.path.exists(check_path):
                actual_file = check_path
                print(f"Found file at: {actual_file}")
                break
        
        # Upload to Webhook if provided (Bypass S3 issues)
        if webhook_url and webhook_url.startswith("http"):
            try:
                print(f"Uploading {p} to {webhook_url}...")
                import requests
                
                # Check if file exists
                if actual_file:
                    with open(actual_file, 'rb') as f:
                        response = requests.post(
                            webhook_url, 
                            files={'file': (os.path.basename(actual_file), f)},
                            data={'jobId': job_id}
                        )
                    print(f"Webhook response: {response.status_code} - {response.text}")
                else:
                    print(f"File not found for webhook: {p}")
                    print(f"Checked paths: {possible_paths}")
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