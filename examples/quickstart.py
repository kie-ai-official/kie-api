        """Minimal Kie.ai example: create one prediction and print the output URL(s)."""
        import kie_api

        output = kie_api.run({
    "prompt": "A cinematic shot of a lighthouse at dawn"
})
        print(output)
