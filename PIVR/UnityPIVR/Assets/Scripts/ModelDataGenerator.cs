using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ModelDataGenerator : MonoBehaviour
{
    public Camera refCam;
    public Transform target;
    public Transform cube;
    public string outputPath;
    public float minDist = 0.1f;
    public float maxDist = 2f;
    public float increment = 0.01f;

    private void Start()
    {

    }

    private void Update()
    {
        float distance = Vector3.Distance(refCam.transform.position, target.position);
        var frustumHeight = 2.0f * distance * Mathf.Tan(refCam.fieldOfView * 0.5f * Mathf.Deg2Rad);
        var frustumWidth = frustumHeight * refCam.aspect;
        Debug.Log(frustumHeight);
        cube.position = target.position;
        cube.localScale = new Vector3(frustumWidth, frustumHeight, cube.localScale.z);
    }
}
