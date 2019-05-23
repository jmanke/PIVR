using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ModelDataGenerator : MonoBehaviour
{
    public Camera refCam;
    public Transform target;
    public string outputPath;
    public float minDist = 0.1f;
    public float maxDist = 2f;
    public float increment = 0.01f;

    private Plane[] planes;
    private Collider objCollider;

    private void Start()
    {
        planes = GeometryUtility.CalculateFrustumPlanes(refCam);
        objCollider = target.GetComponent<Collider>();
    }

    private void Update()
    {
        if (GeometryUtility.TestPlanesAABB(planes, objCollider.bounds))
        {
            Debug.Log(target.name + " has been detected!");
        }
        else
        {
            Debug.Log("Nothing has been detected");
        }
    }
}
