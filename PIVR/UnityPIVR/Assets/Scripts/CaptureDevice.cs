using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;

[RequireComponent(typeof(Camera))]
public class CaptureDevice : MonoBehaviour
{
    public Transform model;
    public Vector2Int cameraResolution = new Vector2Int(640, 480);
    private Vector3 originalModelPos;

    private void Awake()
    {
        originalModelPos = model.position;
    }

    public Texture2D TakeScreenshot()
    {
        var camera = GetComponent<Camera>();
        var rt = new RenderTexture(cameraResolution.x, cameraResolution.y, 24);
        camera.targetTexture = rt;
        var screenShot = new Texture2D(cameraResolution.x, cameraResolution.y, TextureFormat.RGB24, false);
        camera.Render();
        RenderTexture.active = rt;
        screenShot.ReadPixels(new Rect(0, 0, cameraResolution.x, cameraResolution.y), 0, 0);
        camera.targetTexture = null;
        RenderTexture.active = null; // JC: added to avoid errors
        Destroy(rt);

        return screenShot;
    }

    public void ResetModel()
    {
        model.position = originalModelPos;
    }

    /// <summary>
    /// get the two clost points (indices) in the kp pairs list
    /// </summary>
    /// <param name="kpPairs"></param>
    /// <returns></returns>
    private Tuple<int, int> GetFurthestPoints(List<Tuple<Vector2, Vector2>> kpPairs)
    {
        var furthest1 = 0;
        int furthest2 = 0;
        float maxDist = 0f;

        for (int i = 0; i < kpPairs.Count; i++)
        {
            for (int j = 0; j < kpPairs.Count; j++)
            {
                float dist = Vector2.Distance(kpPairs[i].Item1, kpPairs[j].Item1);
                if (dist > maxDist)
                {
                    furthest1 = i;
                    furthest2 = j;
                }
            }
        }

        return new Tuple<int, int>(furthest1, furthest2);
    }

    public void PositionModel(List<Tuple<Vector2, Vector2>> kpPairs)
    {
        if (kpPairs.Count < 2) return;

        var furthestPoints = GetFurthestPoints(kpPairs);

        var cam = GetComponent<Camera>();
        var realPos1 = kpPairs[furthestPoints.Item1].Item2;
        var modelPos1 = kpPairs[furthestPoints.Item1].Item1;

        var realPos2 = kpPairs[furthestPoints.Item2].Item2;
        var modelPos2 = kpPairs[furthestPoints.Item2].Item1;

        float distReal = Vector2.Distance(realPos1, realPos2);
        float distModel = Vector2.Distance(modelPos1, modelPos2);

        var frustumHeight = 2.0f * model.position.z * Mathf.Tan(cam.fieldOfView * 0.5f * Mathf.Deg2Rad);

        var ratio = distModel / distReal;
        var p1Trans = new GameObject("p1").transform;
        var p2Trans = new GameObject("p2").transform;
        p1Trans.SetParent(model);
        p2Trans.SetParent(model);
        p1Trans.position = cam.ScreenToWorldPoint(new Vector3(modelPos1.x, cam.pixelHeight - modelPos1.y, model.position.z));
        p2Trans.position = cam.ScreenToWorldPoint(new Vector3(modelPos2.x, cam.pixelHeight - modelPos2.y, model.position.z));

        var pos = model.position;
        pos.z *= ratio;

        //Debug.Log($"frust height = {frustumHeight}, Ratio = {ratio}");
        //Debug.Log($"Real = {distReal}, Model = {distModel}, Diff = {Mathf.Abs(distReal - distModel)}");

        model.position = pos;
        distModel = Vector3.Distance(cam.WorldToScreenPoint(p1Trans.position), cam.WorldToScreenPoint(p2Trans.position));

        Debug.Log($"AFTER: Real = {distReal}, Model = {distModel}, Diff = {Mathf.Abs(distReal - distModel)}");
        p1Trans.SetParent(null);
        model.SetParent(p1Trans);
        var realScreenPos = new Vector3(realPos1.x, cam.pixelHeight - realPos1.y, model.position.z);
        var modelScreenPos = new Vector3(modelPos1.x, cam.pixelHeight - modelPos1.y, model.position.z);

        var modelKpPos = cam.ScreenToWorldPoint(p1Trans.position) - model.position;
        var targetModelPos = cam.ScreenToWorldPoint(realScreenPos);

        p1Trans.position = targetModelPos;
        model.SetParent(null);

        //Debug.Log("Dist to target = " + Vector3.Distance(cam.transform.position, model.position));

        Destroy(p1Trans.gameObject);
        Destroy(p2Trans.gameObject);
    }
}
