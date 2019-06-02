using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ModelDataGenerator : MonoBehaviour
{
    public Camera refCam;
    public Transform target;
    public Vector2Int cameraResolution = new Vector2Int(1280, 720);
    //public Transform cube;
    public string outputPath;
    public float minDist = 0.2f;
    public float maxDist = 0.4f;
    public int numIncr = 10;
    public int numIncrZ = 5;
    public ModelType modelType = ModelType._2D;

    public enum ModelType
    {
        _3D,
        _2D
    }

    private void Start()
    {
        Debug.Log("Distance = " + Vector3.Distance(refCam.transform.position, target.position));    
        //CaptureScreenshot("manual_image");
        if (modelType == ModelType._2D)
            StartCoroutine(TakePositionSnapshots());
    }

    private void CaptureScreenshot(string imgName)
    {
        var rt = new RenderTexture(cameraResolution.x, cameraResolution.y, 24);
        refCam.targetTexture = rt;
        var screenShot = new Texture2D(cameraResolution.x, cameraResolution.y, TextureFormat.RGB24, false);
        refCam.Render();
        RenderTexture.active = rt;
        screenShot.ReadPixels(new Rect(0, 0, cameraResolution.x, cameraResolution.y), 0, 0);
        refCam.targetTexture = null;
        RenderTexture.active = null; // JC: added to avoid errors
        Destroy(rt);
        byte[] bytes = screenShot.EncodeToJPG();
        string filename = Application.dataPath.Replace("Assets", "") + outputPath + "/" + imgName + ".jpg";
        System.IO.File.WriteAllBytes(filename, bytes);
        Debug.Log("Saved " + filename);
    }

    private IEnumerator TakeRotationScreenshots2D()
    {
        int rotNum = 10;
        float rotIncr = 180f / rotNum;

        for (int i = 0; i < rotNum; i++)
        {
            for (int j = 0; j < rotNum; j++)
            {
                //for (int k = 0; k < rotNum; k++)
                //{
                //    target.eulerAngles = new Vector3(-90f + (rotIncr * j), -90f + (rotIncr * k), -90f + (rotIncr * i));
                //    yield return null;
                //}

                target.eulerAngles = new Vector3(-90f + (rotIncr * i), -90f + (rotIncr * j), 0f);
                yield return null;
            }
        }

        target.eulerAngles = Vector3.zero;
    }

    private IEnumerator TakePositionSnapshots()
    {
        float increment = (maxDist - minDist) / numIncr;
        var originalTargetPos = target.position;

        yield return new WaitForSeconds(0.5f);
        int c = 0;

        for (int i = 0; i < numIncrZ; i++)
        {
            float distance = minDist + (i * increment);
            Vector3[] frustumCorners = new Vector3[4];
            refCam.CalculateFrustumCorners(new Rect(0, 0, 1, 1), distance, Camera.MonoOrStereoscopicEye.Mono, frustumCorners);
            var topLeft = refCam.transform.TransformVector(frustumCorners[1]);
            var bottomLeft = refCam.transform.TransformVector(frustumCorners[0]); 
            var topRight = refCam.transform.TransformVector(frustumCorners[2]);

            // TODO: make numIncr based on size of the current size of the object
            float horIncrAmt = Vector3.Distance(topLeft, topRight) / numIncr;
            float vertIncrAmt = Vector3.Distance(topLeft, bottomLeft) / numIncr;

            for (int j = 0; j < numIncr; j++)
            {
                for (int k = 0; k < numIncr; k++, c++)
                {
                    target.position = new Vector3(topLeft.x + horIncrAmt * k, topLeft.y - vertIncrAmt * j, distance);
                    float dist = Vector3.Distance(target.position, refCam.transform.position);
                    if (Mathf.Abs(dist - 0.85f) < 0.002f)
                    {
                        CaptureScreenshot("img_" + c + "_" + string.Format("{0:00.000}", dist));
                        yield return null;
                    }
                }
            }
        }

        target.position = originalTargetPos;
    }

    void Update()
    {
        // this example shows the different camera frustums when using asymmetric projection matrices (like those used by OpenVR).

        var camera = refCam;
        Vector3[] frustumCorners = new Vector3[4];
        camera.CalculateFrustumCorners(new Rect(0, 0, 1, 1), camera.farClipPlane, Camera.MonoOrStereoscopicEye.Mono, frustumCorners);

        for (int i = 2; i < 3; i++)
        {
            var worldSpaceCorner = camera.transform.TransformVector(frustumCorners[i]);
            Debug.DrawRay(camera.transform.position, worldSpaceCorner, Color.blue);
        }

        camera.CalculateFrustumCorners(new Rect(0, 0, 1, 1), camera.farClipPlane, Camera.MonoOrStereoscopicEye.Left, frustumCorners);

        for (int i = 0; i < 4; i++)
        {
            var worldSpaceCorner = camera.transform.TransformVector(frustumCorners[i]);
            Debug.DrawRay(camera.transform.position, worldSpaceCorner, Color.green);
        }

        camera.CalculateFrustumCorners(new Rect(0, 0, 1, 1), camera.farClipPlane, Camera.MonoOrStereoscopicEye.Right, frustumCorners);

        for (int i = 0; i < 4; i++)
        {
            var worldSpaceCorner = camera.transform.TransformVector(frustumCorners[i]);
            Debug.DrawRay(camera.transform.position, worldSpaceCorner, Color.red);
        }
    }
}