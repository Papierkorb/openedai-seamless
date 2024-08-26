# OpenedAI Text-to-Speech using Seamless

This is a simple script that offers a OpenAI-like API at `/v1/audio/speech` for speech synthesis using [github.com/facebookresearch/seamless_communication](https://github.com/facebookresearch/seamless_communication).

I chose this route as of right now, there aren't many good Text-to-speech engines that support German. The model supports a lot of additional languages, please see the link above.

## Deployment

If you're running bare-bones Docker, you can do this:

```sh
docker build . -t openedai-seamless

# To run on the CPU:
docker run -it --rm -p 3000:3000 openedai-seamless

# To run on a nvidia GPU:
docker run -it --rm -p 3000:3000 --runtime nvidia --gpus all openedai-seamless
```

If you're using docker compose, modify `docker-compose.yml` as you need and then just:

```sh
docker compose up
```

Then test the deployment like this:

```sh
curl 'http://localhost:3000/v1/audio/speech' -H 'Content-Type: application/json' -d '{"input": "Hello from opened AI seamless!", "language": "eng"}' | mpv -
```

## API Support

This service right now only implements the `/v1/audio/speech` interface to some extent.

The expected body looks like this:

```json
{
    "input": "The text that shall be spoken",
    "language": "eng",
    "response_format": "mp3"
}
```

- `input` is simply the text to speak
- `language` is required (!), and is the three-letter language name (E.g. deu, eng, fre, etc.)
- `response_format` defaults to `mp3`, but also allows `flac` and `wav`

Other fields are ignored.

## Further Development

As of right now, this is a not much more than a HTTP wrapper around the "seamless" model. If you're looking for more functionality, I'd be happy to hear from you. Pull Requests are much appreciated!

## License

This code is licensed under the BSD-3 license, see the `LICENSE` file for the complete text.

The model `facebook/seamless-m4t-v2-large` is licensed by Facebook, see here: https://huggingface.co/facebook/seamless-m4t-v2-large - Do note that I'm not affiliated with Facebook in any way shape or form. Also keep in mind that building the Docker image bakes this model into the image itself, which may or may not have legal implications for your use-case.
