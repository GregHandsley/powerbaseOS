import * as React from "react";
import { Button } from "@/components/ui/button";

type Props = {
  onNewDraft: () => void;
  onAddRack: () => void;
  onSave: () => void;
  onPublish: () => void;
  onRename: () => void;
  disabled: boolean;      
  newDraftDisabled?: boolean; 
};

export default function EditorToolbar({
  onNewDraft,
  onAddRack,
  onSave,
  onPublish,
  onRename,
  disabled,
  newDraftDisabled = false,
}: Props) {
  return (
    <div className="flex flex-wrap gap-2">
      <Button onClick={onNewDraft} disabled={newDraftDisabled}>New Draft</Button>
      <Button variant="secondary" onClick={onAddRack} disabled={disabled}>
        Add Rack
      </Button>
      <Button variant="outline" onClick={onSave} disabled={disabled}>
        Save Draft
      </Button>
      <Button variant="default" onClick={onPublish} disabled={disabled}>
        Publish
      </Button>
      <Button variant="secondary" onClick={onRename} disabled={disabled}>
        Rename
      </Button>
    </div>
  );
}