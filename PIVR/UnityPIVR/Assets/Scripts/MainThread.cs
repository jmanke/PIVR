using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;

public class MainThread : MonoBehaviour
{
    public static MainThread Instance;
    private Queue<Tuple<Action<object>, object>> actionQueue = new Queue<Tuple<Action<object>, object>>();

    private void Awake()
    {
        Instance = this;
    }

    public void QueueEvent(Action<object> action, object args)
    {
        actionQueue.Enqueue(new Tuple<Action<object>, object>(action, args));
    }

	// Update is called once per frame
	void Update ()
    {
        while (actionQueue.Count > 0)
        {
            var pair = actionQueue.Dequeue();
            pair.Item1.Invoke(pair.Item2);
        }
    }
}
