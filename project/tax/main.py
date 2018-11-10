import os
import asyncio

# os.system("python a.py")
# os.system("python b.py")

runnable_files = ['credit.py', 'xzcf.py', 'wfaj.py']
async_files = []


def traverse(f):
    fs = os.listdir(f)
    for f1 in fs:
        tmp_path = os.path.join(f, f1)
        if not os.path.isdir(tmp_path):
            print('file: %s' % tmp_path)
            if f1 in runnable_files:
                async_files.append(tmp_path)
                # os.system("python {}".format(tmp_path))
        else:
            print('dir：%s' % tmp_path)
            if f1 == 'all':
                continue
            traverse(tmp_path)


# current_path = os.getcwd()
current_path = os.path.dirname(os.path.dirname(__file__))
print(current_path)
traverse(current_path)
sema = asyncio.Semaphore(30)


async def crawl_command(tmp_path):
    with(await  sema):
        await os.system("python {}".format(tmp_path))


def crawl():
    tasks = []
    for file in async_files:
        tasks.append(crawl_command(file))

    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()


if __name__ == '__main__':
    crawl()
