using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ImageDatasetGenerator : MonoBehaviour
{
    public int numShots = 20;
    public Vector2Int resolution = new Vector2Int(640, 480);
    public Transform model;
    public Collider col;
    public UnityEngine.UI.RawImage backgroundImage;

    public Camera mainCamera;
    public Camera maskCamera;

    public string rootPath = "Datasets";
    public string datasetname = "rasp";
    public string backgroundImagesPath = "E:/uvic/DirectedStudy/PIVR/singleshot6Dpose-master/VOCdevkit/VOC2012/JPEGImages";

    /// <summary>
    /// Range the model can be positioned from the camera
    /// </summary>
    public Vector2 modelRange = new Vector2(0.2f, 2f);
    private Vector3 extents;

    int screenshotCount = 0;

    private string[] imageNames;

    private void Start()
    {
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

    public Vector3[] GetBoundingBox()
    {
        var center = col.bounds.center;
        var points = new Vector3[9];
        var extents = col.bounds.extents;

        // center
        points[0] = center;
        // front
        points[1] = center + model.forward * extents.z - model.up * extents.y + model.right * extents.x;
        points[2] = center + model.forward * extents.z + model.up * extents.y + model.right * extents.x;
        points[3] = center - model.forward * extents.z - model.up * extents.y + model.right * extents.x;
        points[4] = center - model.forward * extents.z + model.up * extents.y + model.right * extents.x;
        // back
        points[5] = center + model.forward * extents.z - model.up * extents.y - model.right * extents.x;
        points[6] = center + model.forward * extents.z + model.up * extents.y - model.right * extents.x;
        points[7] = center - model.forward * extents.z - model.up * extents.y - model.right * extents.x;
        points[8] = center - model.forward * extents.z + model.up * extents.y - model.right * extents.x;

        //corners = np.array([[min_x, min_y, min_z],
        //                    [min_x, min_y, max_z],
        //                    [min_x, max_y, min_z],
        //                    [min_x, max_y, max_z],
        //                    [max_x, min_y, min_z],
        //                    [max_x, min_y, max_z],
        //                    [max_x, max_y, min_z],
        //                    [max_x, max_y, max_z]])

        return points;
    }

    private void SaveLabel(string path, string name)
    {
        var points = GetBoundingBox();

        //foreach (var point in points)
        //{
        //    var obj = GameObject.CreatePrimitive(PrimitiveType.Sphere).GetComponent<Transform>();
        //    obj.localScale = new Vector3(0.01f, 0.01f, 0.01f);
        //    obj.position = point;
        //}

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

        string labelContents = "";

        foreach (var label in labels)
        {
            labelContents += label + " ";
        }

        Debug.Log(labelContents);
        var filename = $"{path}/{name}.txt";
        System.IO.File.WriteAllText(filename, labelContents);
    }

    private bool IsInView(Vector3[] boundingBox)
    {
        var pixelWidth = mainCamera.pixelWidth;
        var pixelHeight = mainCamera.pixelHeight;
        int buffer = 30;

        foreach (var point in boundingBox)
        {
            var screenPos = mainCamera.WorldToScreenPoint(point);
            if (screenPos.x <= buffer || screenPos.y <= buffer || screenPos.x >= pixelWidth - buffer || screenPos.y - buffer >= pixelHeight)
                return false;
        }

        return true;
    }

    /// <summary>
    /// Randomly positions the model within the camera's viewing frustrum 
    /// </summary>
    private void PositionModel()
    {
        // TODO: Calculate a range instead of randomly trying
        do
        {
            model.position = mainCamera.transform.position + mainCamera.transform.forward * Random.Range(modelRange.x, modelRange.y);
            model.rotation = Random.rotation;

            var frustumHeight = 2.0f * Vector3.Distance(mainCamera.transform.position, model.position) * Mathf.Tan(mainCamera.fieldOfView * 0.5f * Mathf.Deg2Rad);
            var frustumWidth = frustumHeight * mainCamera.aspect;

            var modelPosX = Random.Range(-frustumWidth / 2f, frustumWidth / 2f);
            var modelPosY = Random.Range(-frustumHeight / 2f, frustumHeight / 2f);
            model.position = new Vector3(modelPosX, modelPosY, model.position.z);
        } while (!IsInView(GetBoundingBox()));
    }

    public Texture2D LoadJPG(string filePath)
    {

        Texture2D tex = null;
        byte[] fileData;

        if (System.IO.File.Exists(filePath))
        {
            fileData = System.IO.File.ReadAllBytes(filePath);
            tex = new Texture2D(2, 2);
            tex.LoadImage(fileData); //..this will auto-resize the texture dimensions.
        }

        return tex;
    }

    private void CreateDataFile()
    {
        var file = $"{rootPath}/cfg/{datasetname}.data";
        string[] lines =
        {
            $"train  = LINEMOD/{datasetname}/train.txt",
            $"valid  = LINEMOD/{datasetname}/test.txt",
            $"backup = backup/{datasetname}",
            $"mesh = LINEMOD/{datasetname}/{datasetname}.ply",
            $"tr_range = LINEMOD/{datasetname}/training_range.txt",
            $"name = {datasetname}",
            $"diam = 0.10"
        };
        System.IO.File.WriteAllLines(file, lines);
    }

    private IEnumerator GenerateData()
    {
        extents = col.bounds.extents;
        mainCamera.transform.position = Vector3.zero;
        mainCamera.transform.rotation = Quaternion.identity;
        imageNames = System.IO.Directory.GetFiles(backgroundImagesPath, "*.jpg");

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

        CreateDataFile();

        for (int i = 0; i < numShots; i++)
        {
            PositionModel();
            var img = imageNames[Random.Range(0, imageNames.Length - 1)];
            var tex = LoadJPG(img);
            backgroundImage.texture = tex;

            var mainTex = Screenshot.TakeScreenshot(mainCamera, resolution);
            var maskTex = Screenshot.TakeScreenshot(maskCamera, resolution);
            var filename = screenshotCount.ToString("D6");
            images[i] = SaveImageJPG(mainTex, imagesPath, filename);
            SaveLabel(labelsPath, filename);
            var maskName = screenshotCount.ToString("D4");
            SaveMaskPNG(maskTex, maskPath, maskName);
            screenshotCount++;

            yield return null;
        }

        var relImagesPath = $"LINEMOD/{datasetname}/JPEGImages";

        using (var outputFile = new System.IO.StreamWriter(System.IO.Path.Combine(linemodPath, "train.txt")))
        {
            for (int j = 0; j < images.Length; j+=5)
            {
                outputFile.WriteLine($"{relImagesPath}/" + images[j]);
            }
        }

        using (var outputFile = new System.IO.StreamWriter(System.IO.Path.Combine(linemodPath, "test.txt")))
        {
            for (int j = 0; j < images.Length; j ++)
            {
                outputFile.WriteLine($"{relImagesPath}/" + images[j]);
            }
        }
    }
}
