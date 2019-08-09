using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Screenshot
{
    public static Texture2D TakeScreenshot(Camera camera, Vector2Int res)
    {
        var rt = new RenderTexture(res.x, res.y, 24);
        camera.targetTexture = rt;
        var screenShot = new Texture2D(res.x, res.y, TextureFormat.RGB24, false);
        camera.Render();
        RenderTexture.active = rt;
        screenShot.ReadPixels(new Rect(0, 0, res.x, res.y), 0, 0);
        camera.targetTexture = null;
        RenderTexture.active = null; // JC: added to avoid errors
        Object.Destroy(rt);

        return screenShot;
    }
}
