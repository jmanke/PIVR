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
    [Range(0f, 100f)] public float increment = 1f;
    public ModelType modelType = ModelType._2D;

    public enum ModelType
    {
        _3D,
        _2D
    }

    private void Start()
    {
        //StartCoroutine(TakePositionSnapshots());
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
        byte[] bytes = screenShot.EncodeToPNG();
        string filename = Application.dataPath.Replace("Assets", "") + outputPath + "/" + imgName + ".png";
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
        int numIterations = 10;
        float increment = (maxDist - minDist) / numIterations;
        var originalTargetPos = target.position;

        yield return new WaitForSeconds(0.1f);
        int c = 0;

        for (int i = 0; i < numIterations; i++)
        {
            float distance = minDist + (i * increment);
            float frustumHeight = 2.0f * distance * Mathf.Tan(refCam.fieldOfView * 0.5f * Mathf.Deg2Rad);
            float frustumWidth = frustumHeight * refCam.aspect;
            var topLeft = new Vector2(-frustumWidth / 2f, frustumHeight / 2f);

            // TODO: make numIncr based on size of the current size of the object
            float horIncrAmt = frustumWidth / numIncr;
            float vertIncrAmt = frustumHeight / numIncr;

            for (int j = 0; j < numIncr; j++)
            {
                for (int k = 0; k < numIncr; k++, c++)
                {
                    target.position = new Vector3(topLeft.x + horIncrAmt * k, topLeft.y - vertIncrAmt * j, distance);
                    CaptureScreenshot("img_" + c);
                    yield return null;
                }
            }
        }

        target.position = originalTargetPos;
    }
}