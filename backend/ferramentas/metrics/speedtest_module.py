import speedtest

def medir_speedtest():
    try:
        st = speedtest.Speedtest()
        st.get_best_server()

        download = st.download() / 1_000_000  # bits → megabits
        upload = st.upload() / 1_000_000
        ping = st.results.ping

        return {
            "success": True,
            "download_mbps": round(download, 2),
            "upload_mbps": round(upload, 2),
            "ping_ms": round(ping, 2)
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
