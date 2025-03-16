class HeaderPrintingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print("\n--- Request Headers ---")
        for header, value in request.headers.items():
            print(f"{header}: {value}")
        print("--- End Request Headers ---\n")

        response = self.get_response(request)
        return response
