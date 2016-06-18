using System;

public class test {
	public static void Main() {
		System.Net.Sockets.TcpListener listener = new System.Net.Sockets.TcpListener(1234);
		listener.Start();
		Console.WriteLine("listener created");
		System.Net.Sockets.Socket soc = listener.AcceptSocket(); // blocks
		console.WriteLine("connected");
	}
}