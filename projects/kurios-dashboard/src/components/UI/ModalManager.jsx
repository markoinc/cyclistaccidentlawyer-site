import Modal from './Modal';
import useStore from '../../stores/useStore';

export default function ModalManager() {
  const { activeModal, modalData, closeModal } = useStore();

  if (!activeModal) return null;

  // Define modal content based on type
  const getModalContent = () => {
    switch (activeModal) {
      case 'addContact':
        return {
          title: 'Add Contact',
          content: <AddContactForm data={modalData} onClose={closeModal} />
        };
      case 'addProject':
        return {
          title: 'Add Project',
          content: <AddProjectForm data={modalData} onClose={closeModal} />
        };
      case 'addIdea':
        return {
          title: 'Add Idea',
          content: <AddIdeaForm data={modalData} onClose={closeModal} />
        };
      case 'editProspect':
        return {
          title: 'Edit Prospect',
          content: <EditProspectForm data={modalData} onClose={closeModal} />
        };
      case 'viewDetails':
        return {
          title: modalData?.title || 'Details',
          content: <DetailsView data={modalData} />
        };
      default:
        return {
          title: 'Modal',
          content: <div>Unknown modal type: {activeModal}</div>
        };
    }
  };

  const { title, content } = getModalContent();

  return (
    <Modal title={title} onClose={closeModal} size="lg">
      {content}
    </Modal>
  );
}

// Placeholder form components - implement as needed
function AddContactForm({ onClose }) {
  const { settings } = useStore();
  const darkMode = settings.appearance.darkMode;
  
  return (
    <div className="space-y-4">
      <p className={darkMode ? 'text-gray-300' : 'text-gray-600'}>
        Contact form coming soon...
      </p>
      <button
        onClick={onClose}
        className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
      >
        Close
      </button>
    </div>
  );
}

function AddProjectForm({ onClose }) {
  const { settings } = useStore();
  const darkMode = settings.appearance.darkMode;
  
  return (
    <div className="space-y-4">
      <p className={darkMode ? 'text-gray-300' : 'text-gray-600'}>
        Project form coming soon...
      </p>
      <button
        onClick={onClose}
        className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
      >
        Close
      </button>
    </div>
  );
}

function AddIdeaForm({ onClose }) {
  const { settings } = useStore();
  const darkMode = settings.appearance.darkMode;
  
  return (
    <div className="space-y-4">
      <p className={darkMode ? 'text-gray-300' : 'text-gray-600'}>
        Idea form coming soon...
      </p>
      <button
        onClick={onClose}
        className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
      >
        Close
      </button>
    </div>
  );
}

function EditProspectForm({ data, onClose }) {
  const { settings } = useStore();
  const darkMode = settings.appearance.darkMode;
  
  return (
    <div className="space-y-4">
      <p className={darkMode ? 'text-gray-300' : 'text-gray-600'}>
        Editing: {data?.name || 'Unknown'}
      </p>
      <button
        onClick={onClose}
        className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
      >
        Close
      </button>
    </div>
  );
}

function DetailsView({ data }) {
  const { settings } = useStore();
  const darkMode = settings.appearance.darkMode;
  
  return (
    <div className={`space-y-2 ${darkMode ? 'text-gray-300' : 'text-gray-600'}`}>
      <pre className="text-sm overflow-auto max-h-96">
        {JSON.stringify(data, null, 2)}
      </pre>
    </div>
  );
}
