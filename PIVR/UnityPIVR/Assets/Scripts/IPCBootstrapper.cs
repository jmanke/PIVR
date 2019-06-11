using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Threading;

public class IPCBootstrapper : MonoBehaviour
{
    Server server;
    public CaptureDevice cd;

	// Use this for initialization
	void Start ()
    {
        server = new Server(cd);
        server.testImg = cd.TakeScreenshot().EncodeToJPG();

        var thr = new Thread(new ThreadStart(server.Start));
        thr.Start();

        Debug.Log("Start thread");
	}

    public void OnDestroy()
    {
        server.alive = false;
    }
}
