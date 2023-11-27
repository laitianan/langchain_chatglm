from watchdog.events import FileSystemEventHandler
import logging

from global_config import ChatConfig


class FileEventHandler(FileSystemEventHandler):
    """Logs all the events captured."""

    def on_moved(self, event):
        super(FileEventHandler, self).on_moved(event)

        what = 'directory' if event.is_directory else 'file'
        logging.info("Moved %s: from %s to %s", what, event.src_path,
                     event.dest_path)

    def on_created(self, event):
        super(FileEventHandler, self).on_created(event)

        what = 'directory' if event.is_directory else 'file'
        logging.info("Created %s: %s", what, event.src_path)

    def on_deleted(self, event):
        super(FileEventHandler, self).on_deleted(event)

        what = 'directory' if event.is_directory else 'file'
        logging.info("Deleted %s: %s", what, event.src_path)

    def on_modified(self, event):
        global agent_exec, toos_dict, llm, initparam, search
        super(FileEventHandler, self).on_modified(event)
        chatconfig = ChatConfig()
        chatconfig.initparam()
        # agent_exec, toos_dict, llm, initparam, search = chatconfig.get_init()
        what = 'directory' if event.is_directory else 'file'
        logging.info("Modified %s: %s", what, event.src_path)