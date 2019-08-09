using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class DatasetGenerator : MonoBehaviour
{
    public float timeBetweenShots = 0.5f;
    public int numShots = 20;
    public Vector2Int resolution = new Vector2Int(640, 480);
    public Transform model;
    public Transform test;

    public Camera mainCamera;
    public Camera maskCamera;

    public string rootPath = "Datasets";
    public string datasetname = "rasp";

    string frmt;
    int screenshotCount = 0;

    bool pause = false;
    Vector3 lastCamPos;
    Quaternion lastCamRot;

    private void Start()
    {
        mainCamera.gameObject.AddComponent<FollowEditorCamera>();
        StartCoroutine(GenerateData());
    }

    private string SaveImageJPG(Texture2D tex, string path, string name)
    {
        byte[] bytes = tex.EncodeToJPG();
        var filename = $"{path}/{name}.jpg";
        System.IO.File.WriteAllBytes(filename, bytes);
        Debug.Log("Saved " + filename);
        return name + ".jpg";
    }

    private void SaveMaskPNG(Texture2D tex, string path, string name)
    {
        byte[] bytes = tex.EncodeToPNG();
        var filename = $"{path}/{name}.png";
        System.IO.File.WriteAllBytes(filename, bytes);
        Debug.Log("Saved " + filename);
    }

    private bool SaveLabel(string path, string name)
    {
        var col = model.GetComponent<Collider>();
        var extents = col.bounds.extents;
        var center = col.bounds.center;
        var points = new Vector3[9];

        // center
        points[0] = center;

        // front 
        points[1] = center + model.forward * extents.z - model.up * extents.y - model.right * extents.x;
        points[2] = center + model.forward * extents.z + model.up * extents.y - model.right * extents.x;
        points[3] = center + model.forward * extents.z - model.up * extents.y + model.right * extents.x;
        points[4] = center + model.forward * extents.z + model.up * extents.y + model.right * extents.x;
        // back
        points[5] = center - model.forward * extents.z - model.up * extents.y - model.right * extents.x;
        points[6] = center - model.forward * extents.z + model.up * extents.y - model.right * extents.x;
        points[7] = center - model.forward * extents.z - model.up * extents.y + model.right * extents.x;
        points[8] = center - model.forward * extents.z + model.up * extents.y + model.right * extents.x;

        var labels = new float[21];
        float horMin = 1f;
        float horMax = 0f;
        float vertMin = 1f;
        float vertMax = 0f;
        labels[0] = 0;

        for (int i = 0; i < points.Length; i++)
        {
            var screenPos = mainCamera.WorldToScreenPoint(points[i]);
            float xPos = screenPos.x / resolution.x;
            float yPos = 1f - (screenPos.y / resolution.y);

            labels[i * 2 + 1] = xPos;
            labels[i * 2 + 2] = yPos;

            if (xPos < 0.1f || xPos > 0.9f || yPos < 0.1f || yPos > 0.9f)
            {
                Debug.Log("Out of range");
                return false;
            }

            if (xPos < horMin)
                horMin = xPos;
            if (xPos > horMax)
                horMax = xPos;
            if (yPos < vertMin)
                vertMin = yPos;
            if (yPos > vertMax)
                vertMax = yPos;
        }

        labels[19] = horMax - horMin;
        labels[20] = vertMax - vertMin;

        if (labels[19] < 0.1f || labels[19] > 0.5f || labels[20] < 0.1f || labels[20] > 0.9f)
        {
            Debug.LogError("BAD RANGE");
            return false;
        }

        string labelContents = "";

        foreach (var label in labels)
        {
            labelContents += label + " ";
        }

        Debug.Log(labelContents);
        var filename = $"{path}/{name}.txt";
        System.IO.File.WriteAllText(filename, labelContents);

        return true;
    }

    private IEnumerator GenerateData()
    {
        yield return new WaitForSeconds(1f);
        var images = new string[numShots];

        var linemodPath = $"{rootPath}/LINEMOD/{datasetname}";
        var imagesPath = $"{linemodPath}/JPEGImages";
        var labelsPath = $"{linemodPath}/labels";
        var maskPath = $"{linemodPath}/mask";

        // Create directories if they don't exist
        if (!System.IO.Directory.Exists(linemodPath))
            System.IO.Directory.CreateDirectory(linemodPath);
        if (!System.IO.Directory.Exists(imagesPath))
            System.IO.Directory.CreateDirectory(imagesPath);
        if (!System.IO.Directory.Exists(labelsPath))
            System.IO.Directory.CreateDirectory(labelsPath);
        if (!System.IO.Directory.Exists(maskPath))
            System.IO.Directory.CreateDirectory(maskPath);

        int i;

        for (i = 0; i < numShots; i++)
        {
            // Only take screenshots if the camera is in a different orientation than the last shot
            while (lastCamRot == mainCamera.transform.rotation && lastCamPos == mainCamera.transform.position)
                yield return null;

            var mainTex = Screenshot.TakeScreenshot(mainCamera, resolution);
            var maskTex = Screenshot.TakeScreenshot(maskCamera, resolution);
            var filename = screenshotCount.ToString("D6");

            if (!SaveLabel(labelsPath, filename))
            {
                i--;
                Debug.Log("BAD");
                yield return new WaitForSeconds(timeBetweenShots);
                continue;
            }

            images[i] = SaveImageJPG(mainTex, imagesPath, filename);
            SaveLabel(labelsPath, filename);
            var maskName = screenshotCount.ToString("D4");
            SaveMaskPNG(maskTex, maskPath, maskName);
            screenshotCount++;
            lastCamPos = mainCamera.transform.position;
            lastCamRot = mainCamera.transform.rotation;

            while (pause)
                yield return null;

            yield return new WaitForSeconds(timeBetweenShots);
        }

        var relImagesPath = $"LINEMOD/{datasetname}/JPEGImages";

        using (var outputFile = new System.IO.StreamWriter(System.IO.Path.Combine(linemodPath, "train.txt")))
        {
            for (int j = 0; j < images.Length; j++)
            {
                outputFile.WriteLine($"{relImagesPath}/" + images[j]);
            }
        }

        using (var outputFile = new System.IO.StreamWriter(System.IO.Path.Combine(linemodPath, "test.txt")))
        {
            for (int j = 0; j < images.Length; j+=3)
            {
                outputFile.WriteLine($"{relImagesPath}/" + images[j]);
            }
        }
    }

    private void Update()
    {
        if (Input.GetKeyDown(KeyCode.P))
        {
            pause = !pause;
            Debug.Log("Paused: " + pause);
        }
    }
}
