import SwiftUI

struct ContentView: View {
    @State private var selectedFolder: String? = nil
    @State private var selectedNote: String? = nil
    
    var body: some View {
        NavigationView {
            // Left Sidebar (Folders)
            SidebarView(selectedFolder: $selectedFolder)
            
            // Middle Panel (Notes List)
            NoteListView(selectedNote: $selectedNote)
            
            // Right Panel (Note Editor)
            NoteEditorView(noteContent: .constant(""))
        }
        .toolbar {
            ToolbarItemGroup {
                Button(action: {}) {
                    Image(systemName: "square.and.pencil")
                }
                Button(action: {}) {
                    Image(systemName: "photo")
                }
                Button(action: {}) {
                    Image(systemName: "table")
                }
                Button(action: {}) {
                    Image(systemName: "text.alignleft")
                }
            }
        }
    }
}

struct SidebarView: View {
    @Binding var selectedFolder: String?
    
    var body: some View {
        List {
            Section(header: Text("iCloud")) {
                NavigationLink(
                    destination: Text("iCloud Notes"),
                    tag: "iCloud",
                    selection: $selectedFolder
                ) {
                    Label("iCloud 全部备忘录", systemImage: "doc.text")
                }
            }
            
            Section(header: Text("Folders")) {
                ForEach(["备忘录", "57Blocks", "读书笔记", "今日头条"], id: \.self) { folder in
                    NavigationLink(
                        destination: Text(folder),
                        tag: folder,
                        selection: $selectedFolder
                    ) {
                        Label(folder, systemImage: "folder")
                    }
                }
            }
        }
        .listStyle(SidebarListStyle())
    }
}

struct NoteListView: View {
    @Binding var selectedNote: String?
    
    var body: some View {
        List {
            ForEach(1...10, id: \.self) { index in
                NavigationLink(
                    destination: Text("Note \(index)"),
                    tag: "Note \(index)",
                    selection: $selectedNote
                ) {
                    VStack(alignment: .leading) {
                        Text("Note \(index)")
                            .font(.headline)
                        Text("Last modified: 2024-12-12")
                            .font(.caption)
                            .foregroundColor(.gray)
                    }
                    .padding(.vertical, 4)
                }
            }
        }
    }
}

struct NoteEditorView: View {
    @Binding var noteContent: String
    
    var body: some View {
        TextEditor(text: $noteContent)
            .padding()
    }
}

#Preview {
    ContentView()
}
