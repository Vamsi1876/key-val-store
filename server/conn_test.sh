$client = New-Object System.Net.Sockets.TcpClient("localhost", 6740)
$stream = $client.GetStream()
$writer = New-Object System.IO.StreamWriter($stream)
$writer.AutoFlush = $true
$reader = New-Object System.IO.StreamReader($stream)

$writer.WriteLine("SET name vamsi")
$reader.ReadLine()
