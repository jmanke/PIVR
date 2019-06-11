using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class Test : MonoBehaviour
{
    public RectTransform target;

    public void Sync()
    {
        var cam = Camera.main;
        Debug.Log(Input.mousePosition);
        var mousePos = Input.mousePosition;
        mousePos.z = transform.position.z;
        var pos = cam.ScreenToWorldPoint(mousePos);
        pos.z = 10f;
        Debug.Log(pos);
        transform.position = pos;
    }

    public void Update()
    {
        Sync();
    }
}
