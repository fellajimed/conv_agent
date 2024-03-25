import argparse
from .agent import ConvAgent


def main():
    parser = argparse.ArgumentParser('main')
    parser.add_argument('--url', type=str, required=True)
    parser.add_argument('--model', type=str, default=None)
    parser.add_argument('--content', type=str, default=None)
    parser.add_argument('--plain', action='store_true')
    parser.add_argument('--width', type=int, default=None)
    parser.add_argument('-n', type=int, default=1)
    parser.add_argument('-I', '--interactive', action='store_true')
    parser.add_argument('--prompt', type=str)

    args = parser.parse_args()

    agent = ConvAgent(url=args.url, model=args.model,
                      content_prompt=args.content, n=args.n,
                      width=args.width, is_table=not args.plain)

    if args.interactive or args.prompt is None:
        agent.start_conversation()
    else:
        agent.formatter.answer(agent.get_answer(args.prompt))


if __name__ == "__main__":
    raise SystemExit(main())
