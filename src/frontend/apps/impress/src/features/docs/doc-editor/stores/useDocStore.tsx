import { BlockNoteEditor } from '@blocknote/core';
import { HocuspocusProvider } from '@hocuspocus/provider';
import * as Y from 'yjs';
import { create } from 'zustand';

import { providerUrl } from '@/core';
import { Base64, Doc } from '@/features/docs/doc-management';

import { blocksToYDoc } from '../utils';

interface DocStore {
  provider: HocuspocusProvider;
  editor?: BlockNoteEditor;
}

export interface UseDocStore {
  currentDoc?: Doc;
  docsStore: {
    [storeId: string]: DocStore;
  };
  createProvider: (storeId: string, initialDoc: Base64) => HocuspocusProvider;
  setStore: (storeId: string, props: Partial<DocStore>) => void;
  setCurrentDoc: (doc: Doc | undefined) => void;
}

export const useDocStore = create<UseDocStore>((set, get) => ({
  currentDoc: undefined,
  docsStore: {},
  createProvider: (storeId: string, initialDoc: Base64) => {
    const doc = new Y.Doc({
      guid: storeId,
    });

    if (initialDoc) {
      Y.applyUpdate(doc, Buffer.from(initialDoc, 'base64'));
    } else {
      const initialDocContent = [
        {
          type: 'heading',
          content: '',
        },
      ];

      blocksToYDoc(initialDocContent, doc);
    }

    const provider = new HocuspocusProvider({
      url: providerUrl(storeId),
      name: storeId,
      document: doc,
    });

    get().setStore(storeId, { provider });

    return provider;
  },
  setStore: (storeId, props) => {
    set(({ docsStore }, ...store) => {
      return {
        ...store,
        docsStore: {
          ...docsStore,
          [storeId]: {
            ...docsStore[storeId],
            ...props,
          },
        },
      };
    });
  },
  setCurrentDoc: (doc) => {
    set({ currentDoc: doc });
  },
}));
